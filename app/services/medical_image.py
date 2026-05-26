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

        prompt = self._build_prompt(content)
        logger.debug("Image prompt (%s): %.300s", self.settings.ai_provider, prompt)

        try:
            if self.settings.ai_provider == "gemini":
                return await self._generate_with_gemini(content, prompt)
            return await self._generate_with_openai(content, prompt)
        except Exception as exc:
            logger.warning("Image generation failed (%s): %s", self.settings.ai_provider, exc)
            return None

    # ── Gemini / Imagen 3 ──────────────────────────────────────────────────────

    async def _generate_with_gemini(self, content: GeneratedContent, prompt: str) -> Path | None:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=self.settings.gemini_api_key)
        model = self.settings.gemini_image_model  # imagen-3.0-generate-002

        response = await client.aio.models.generate_images(
            model=model,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="3:4",        # portrait — matches 1080×1500 poster
                guidance_scale=8.5,        # strong prompt adherence
                add_watermark=False,
                negative_prompt=(
                    "blurry, low quality, watermark, logo, text overlay, "
                    "cartoon style, anime, abstract art, impressionist, "
                    "real patient face, copyrighted material, branded content"
                ),
            ),
        )

        if not response.generated_images:
            logger.warning("Imagen 3 returned no images.")
            return None

        image_bytes = response.generated_images[0].image.image_bytes
        if not image_bytes:
            logger.warning("Imagen 3 image has no bytes.")
            return None

        path = self.settings.generated_dir / f"visual_{_subject_key(content)}_{uuid4().hex[:8]}.png"
        path.write_bytes(image_bytes)
        logger.info("Imagen 3 medical visual saved: %s", path)
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

    def _build_prompt(self, content: GeneratedContent) -> str:
        subj_key = _subject_key(content)
        fmt_key = content.content_format.value

        subject_style = _SUBJECT_VISUAL_STYLE.get(
            subj_key, "medical education illustration, clean schematic style"
        )
        format_guidance = _FORMAT_VISUAL_GUIDANCE.get(
            fmt_key, "clear educational medical diagram, labelled structures"
        )

        topic = content.poster_text or content.title or subj_key.replace("_", " ")
        visual_desc = content.visual_description or ""
        labels = ", ".join((content.visual_labels or content.image_based_data or [])[:4])
        subject_display = subj_key.replace("_", " ").title()

        prompt = (
            f"Medical education illustration for {subject_display}: {topic}. "
            f"Visual style: {subject_style}. "
            f"Purpose: {format_guidance}. "
        )
        if visual_desc:
            prompt += f"Specific visual requirement: {visual_desc}. "
        if labels:
            prompt += (
                f"The image must clearly show and label these features: {labels}. "
                "Each labelled feature must be visually distinct and identifiable. "
            )

        prompt += f"{_ACCURACY_BLOCK} {_STYLE_BLOCK} {_SAFETY_BLOCK}"
        return prompt[:4000]


def _subject_key(content: GeneratedContent) -> str:
    if content.subject:
        return content.subject.value
    if content.news_topic:
        return content.news_topic.value
    return "general_medicine"
