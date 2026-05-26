"""
Medical image generator.

Supports two backends:
  - Gemini / Imagen 3  (ai_provider="gemini", gemini_api_key set)
  - OpenAI DALL-E / GPT-Image  (ai_provider="openai", openai_api_key set)

Set GENERATE_REALISTIC_IMAGES=true in .env to activate either backend.
The Gemini / Imagen 3 path is the recommended default when a Gemini API key
is available: it produces photorealistic medical education illustrations at
no extra image-API cost beyond the generative AI quota.
"""
from __future__ import annotations

import base64
import logging
from pathlib import Path
from uuid import uuid4

from app.config import Settings
from app.models import GeneratedContent

logger = logging.getLogger(__name__)

# ── Subject-specific visual style descriptors ──────────────────────────────────

_SUBJECT_VISUAL_STYLE: dict[str, str] = {
    "anatomy": (
        "detailed anatomical cross-section illustration, medical textbook style, "
        "labelled structures, white background, high-contrast line art with "
        "colour-coded tissue layers, Netter-style illustration"
    ),
    "physiology": (
        "physiology diagram — accurate graph axes, schematic of a physiological "
        "process (e.g. oxygen-dissociation curve, cardiac cycle, nerve action "
        "potential), clean educational infographic style"
    ),
    "biochemistry": (
        "metabolic pathway diagram, enzyme-substrate interaction schematic, "
        "colour-coded molecules, clear directional arrows, textbook biochemistry "
        "illustration style (similar to Lehninger or Harper)"
    ),
    "pathology": (
        "histopathology-inspired educational schematic, circular microscopy field "
        "of view, labelled pathological features, H&E stain colour palette "
        "(pink cytoplasm, purple/dark nuclei), Robbins pathology style"
    ),
    "pharmacology": (
        "drug mechanism of action diagram, receptor-ligand binding schematic, "
        "dose-response curve with labelled EC50 and Emax, molecular pharmacology "
        "educational illustration"
    ),
    "microbiology": (
        "microbiology educational diagram, Gram stain or Ziehl-Neelsen stain "
        "representation, circular microscopy field with labelled micro-organisms "
        "(correct morphology — cocci, bacilli, spirochetes as appropriate), "
        "clinical microbiology textbook style"
    ),
    "forensic_medicine": (
        "forensic medicine educational schematic, body chart or injury-pattern "
        "diagram, clinical forensic illustration, no graphic content, "
        "educational context only"
    ),
    "community_medicine": (
        "public health infographic — epidemiology diagram, 2×2 contingency table, "
        "epidemic curve, or screening flow chart, clean data-visualisation style"
    ),
    "general_medicine": (
        "clinical medicine educational schematic — ECG trace with PQRST labelled, "
        "chest auscultation zones, or physical examination sign illustration, "
        "Harrison's Principles style"
    ),
    "general_surgery": (
        "surgical anatomy educational illustration — operative field diagram, "
        "schematic plain X-ray or CT finding, clean clinical illustration "
        "on white background"
    ),
    "obstetrics_gynecology": (
        "obstetrics educational schematic — partograph with alert/action lines, "
        "fetal lie and presentation diagram, or pelvic anatomy cross-section, "
        "Williams Obstetrics textbook style"
    ),
    "pediatrics": (
        "paediatrics educational illustration — WHO growth chart (weight-for-age), "
        "clinical assessment schematic, or IMCI classification chart, "
        "friendly and clear medical style"
    ),
    "ophthalmology": (
        "ophthalmology educational diagram — fundus schematic with labelled disc "
        "and vessels, eye cross-section (cornea, lens, retina, optic nerve), or "
        "visual field defect map, Kanski Clinical Ophthalmology style"
    ),
    "ent": (
        "ENT educational diagram — otoscopic tympanic membrane view with labelled "
        "cone of light, malleus, and perforation (if relevant); or endoscopic "
        "nasal passage schematic; audiogram, otolaryngology textbook style"
    ),
    "orthopedics": (
        "orthopaedics educational diagram — joint anatomy cross-section, AO fracture "
        "classification schematic, or X-ray pattern illustration with labelled "
        "key radiological sign, clean clinical style"
    ),
    "dermatology": (
        "dermatology educational illustration — skin lesion morphology diagram, "
        "skin cross-section showing all layers with labelled lesion type, or "
        "dermatoscopy pattern schematic, Fitzpatrick's Dermatology style"
    ),
    "psychiatry": (
        "psychiatry educational schematic — lateral brain diagram with labelled "
        "lobes and limbic structures, neurotransmitter pathway illustration, "
        "or DSM clinical assessment flow chart"
    ),
    "radiology": (
        "radiology educational schematic — PA chest X-ray with labelled findings "
        "(lung fields, heart borders, mediastinum, costophrenic angles), or "
        "CT cross-section diagram, classic black-and-white X-ray illustration "
        "style with annotations"
    ),
    "anesthesiology": (
        "anaesthesiology educational diagram — airway anatomy sagittal cross-section "
        "with laryngoscopy view, Mallampati classification, or anaesthetic circuit "
        "schematic, Miller's Anesthesia textbook style"
    ),
}

_FORMAT_VISUAL_GUIDANCE: dict[str, str] = {
    "mcq": (
        "single dominant diagnostic clue clearly visible; supporting context in the "
        "background; designed for a clinical vignette image-based question"
    ),
    "image_based_question": (
        "high-detail diagnostic image, the single most important pathological or "
        "anatomical finding prominently centred and in sharp focus; supporting "
        "structures visible for anatomical context; one 'key clue' highlighted "
        "with a subtle colour contrast or arrow"
    ),
    "rapid_revision": (
        "clean summary diagram with the key concept illustrated and all major "
        "components labelled; designed for rapid recognition, not decoration"
    ),
    "concise_notes": (
        "educational summary card style; key points illustrated with simple icons "
        "or diagrams on a white background"
    ),
    "clinical_case": (
        "clinical scenario schematic showing the presenting signs or the relevant "
        "investigation finding; patient-centred, no identifying features"
    ),
    "pyq_concept": (
        "NEET-PG frequently tested concept illustrated — the 'classic' exam image "
        "that recurs across previous year questions"
    ),
    "flashcard": (
        "single clear illustration on white background, one dominant concept, "
        "minimal background clutter — suitable for flashcard front"
    ),
    "mnemonic": (
        "visual mnemonic aid — colour-coded components corresponding to each letter "
        "of the mnemonic, memorable and spatially organised"
    ),
    "true_false": (
        "clear factual illustration of the stated concept for visual confirmation "
        "or refutation; labelled diagram"
    ),
    "one_liner_recall": (
        "minimal focused diagram highlighting the single fact to recall; "
        "one key structure or process, clearly labelled"
    ),
    "practical_viva": (
        "examination finding schematic — demonstrates the clinical sign that would "
        "be asked in a viva, with the key feature annotated"
    ),
}

_ACCURACY_BLOCK = (
    "ACCURACY REQUIREMENTS: "
    "Anatomy must be correct — correct number of structures, correct relative "
    "positions and proportions. "
    "If showing an ECG, the PQRST morphology must be physiologically plausible. "
    "If showing a histology field, cell morphology must match the stated diagnosis. "
    "If showing an X-ray, density, distribution, and anatomical relationships must "
    "be radiologically plausible. "
    "If showing a graph, axes, curve shape, and labels must be scientifically accurate. "
    "No fantasy anatomy. No placeholder geometric shapes instead of real structures."
)

_STYLE_BLOCK = (
    "STYLE: Clean, high-contrast, professional medical education illustration. "
    "White or very light neutral background. Precise line art with accurate proportions. "
    "Colour is used purposefully — highlight the key diagnostic feature in a contrasting "
    "colour; supporting structures in softer tones. "
    "Text labels, if present, must be in English, legible, and correctly spelled. "
    "No watermarks, no logos, no branded content, no copyright symbols. "
    "Sharp focus throughout — no painting effects or soft blurring."
)

_SAFETY_BLOCK = (
    "IMPORTANT: Educational use only. "
    "Do not include identifiable patient photographs. "
    "Do not reproduce any copyrighted figure, textbook plate, or branded courseware. "
    "Use original schematic / diagram style only."
)


class MedicalImageGenerator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def configured(self) -> bool:
        if not self.settings.generate_realistic_images:
            return False
        p = self.settings.ai_provider
        return (
            (p == "gemini" and bool(self.settings.gemini_api_key))
            or (p == "openai" and bool(self.settings.openai_api_key))
        )

    async def create_visual(self, content: GeneratedContent) -> Path | None:
        if not self.configured:
            return None

        # Use Gemini to write a specific visual description, then generate via Pollinations
        visual_query = await self._get_visual_query(content)
        prompt = self._build_prompt(content, visual_query)
        logger.debug("Image prompt: %.300s", prompt)

        try:
            if self.settings.ai_provider == "gemini":
                return await self._generate_with_gemini(content, prompt)
            return await self._generate_with_openai(content, prompt)
        except Exception as exc:
            logger.warning("Image generation failed (%s): %s", self.settings.ai_provider, exc)
            return None

    async def _get_visual_query(self, content: GeneratedContent) -> str:
        """Ask Gemini to describe what the image should show for this specific topic."""
        try:
            from google import genai

            client = genai.Client(api_key=self.settings.gemini_api_key)
            topic = content.title or content.poster_text or ""
            subject = _subject_key(content).replace("_", " ")

            response = await client.aio.models.generate_content(
                model=self.settings.gemini_text_model,
                contents=(
                    f"Write a 10-word image description for a medical education illustration about "
                    f"'{topic}' ({subject}). Focus on the specific anatomical structure, "
                    f"pathological finding, or clinical concept that should be visualised. "
                    f"Example outputs: 'brachial plexus C5 C6 nerve roots shoulder anatomy' / "
                    f"'H&E slide coagulative necrosis ghost cells eosinophilic' / "
                    f"'Mallampati airway classification oral cavity uvula'. "
                    f"Reply with ONLY the description, no punctuation, no explanation."
                ),
            )
            query = (response.text or "").strip().split("\n")[0][:150]
            logger.debug("Gemini visual query for '%s': %s", topic, query)
            return query
        except Exception as exc:
            logger.debug("Visual query generation failed, using fallback: %s", exc)
            return content.title or content.poster_text or _subject_key(content).replace("_", " ")

    # ── Gemini / Imagen 3 ──────────────────────────────────────────────────────

    async def _generate_with_gemini(self, content: GeneratedContent, prompt: str) -> Path | None:
        """Generate via Pollinations.ai (FLUX model, free, no API key required).

        Google's image APIs (Imagen 3 and Gemini Flash image generation) both
        require paid billing beyond the free text tier, so we use Pollinations
        as the image backend when the provider is set to Gemini.
        """
        import urllib.parse

        import httpx

        short_prompt = prompt[:600]
        encoded = urllib.parse.quote(short_prompt)
        seed = abs(hash(short_prompt)) % 99999
        url = (
            f"https://image.pollinations.ai/prompt/{encoded}"
            f"?width=1024&height=1024&model=flux-pro&nologo=true&seed={seed}"
        )

        logger.info("Generating medical visual via Pollinations.ai (FLUX)…")
        try:
            async with httpx.AsyncClient(timeout=90, follow_redirects=True) as client:
                response = await client.get(url)
                response.raise_for_status()
        except Exception as exc:
            logger.error("Pollinations image generation failed: %s", exc, exc_info=True)
            return None

        content_type = response.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            logger.warning("Pollinations returned non-image content-type: %s", content_type)
            return None

        path = self.settings.generated_dir / f"visual_{_subject_key(content)}_{uuid4().hex[:8]}.png"
        path.write_bytes(response.content)
        logger.info("Pollinations visual saved: %s (%d bytes)", path, len(response.content))
        return path

    # ── OpenAI DALL-E / GPT-Image ─────────────────────────────────────────────

    async def _generate_with_openai(self, content: GeneratedContent, prompt: str) -> Path | None:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        response = await client.images.generate(
            model=self.settings.openai_image_model,
            prompt=prompt,
            size=self.settings.openai_image_size,
            quality=self.settings.openai_image_quality,
            n=1,
        )

        image_data = response.data[0].b64_json if response.data else None
        if not image_data:
            logger.warning("OpenAI image generation returned no base64 payload.")
            return None

        path = self.settings.generated_dir / f"visual_{_subject_key(content)}_{uuid4().hex[:8]}.png"
        path.write_bytes(base64.b64decode(image_data))
        logger.info("OpenAI medical visual saved: %s", path)
        return path

    # ── Prompt builder ─────────────────────────────────────────────────────────

    def _build_prompt(self, content: GeneratedContent, visual_query: str = "") -> str:
        """Build a FLUX-optimised prompt: modality anchors style, Gemini query provides specificity."""
        subj_key = _subject_key(content)
        modality = _SUBJECT_MODALITY.get(subj_key, "medical education diagram")
        labels = (content.visual_labels or content.image_based_data or [])[:3]

        # visual_query from Gemini is the most specific signal — put it right after modality
        core = visual_query or content.title or content.poster_text or subj_key.replace("_", " ")

        parts = [modality, core]
        if labels:
            parts.append("labeled: " + ", ".join(labels))
        parts.append("educational, clean white background, no text overlay, no watermark")

        return ", ".join(parts)[:450]


# Modality-first descriptors — anchors FLUX to the right visual domain
_SUBJECT_MODALITY: dict[str, str] = {
    "anatomy":               "labeled anatomical cross-section diagram, color-coded tissue layers, Netter medical atlas style",
    "physiology":            "physiology graph or process schematic with labeled axes, clean educational infographic",
    "biochemistry":          "biochemical pathway diagram, color-coded molecules, directional arrows",
    "pathology":             "histopathology microscope slide H&E stain, pink eosinophilic cytoplasm, purple nuclei, circular field of view",
    "pharmacology":          "pharmacology dose-response curve or receptor mechanism diagram, labeled axes",
    "microbiology":          "microbiology microscopy Gram stain, labeled bacteria morphology, circular microscope field",
    "forensic_medicine":     "forensic body chart injury pattern diagram, anatomical illustration",
    "community_medicine":    "epidemiology infographic or 2x2 contingency table, clean data-visualization style",
    "general_medicine":      "medical ECG tracing with labeled PQRST waves, or clinical examination schematic",
    "general_surgery":       "surgical anatomy diagram, operative field illustration, labeled structures",
    "obstetrics_gynecology": "obstetrics diagram fetal lie or pelvic anatomy cross-section, labeled",
    "pediatrics":            "pediatric growth chart or clinical assessment schematic, clear labels",
    "ophthalmology":         "ophthalmology fundus diagram or eye cross-section, labeled disc vessels retina",
    "ent":                   "otoscopic tympanic membrane view labeled, or nasal anatomy cross-section",
    "orthopedics":           "orthopedic joint anatomy or fracture classification schematic, labeled X-ray style",
    "dermatology":           "skin layers cross-section diagram, labeled lesion morphology, dermoscopy pattern",
    "psychiatry":            "lateral brain diagram labeled lobes and limbic structures, neurotransmitter pathway",
    "radiology":             "PA chest X-ray with labeled findings, black and white radiograph, annotated landmarks",
    "anesthesiology":        "airway anatomy sagittal cross-section, laryngoscopy view, Mallampati classification diagram",
}


def _subject_key(content: GeneratedContent) -> str:
    if content.subject:
        return content.subject.value
    if content.news_topic:
        return content.news_topic.value
    return "general_medicine"
