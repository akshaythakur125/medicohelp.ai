"""
Medical image generator — calls an AI image API when configured.

Prompt engineering: specialty-specific, high-detail, clinically accurate
prompts tailored to each MBBS subject and content format.
"""
from __future__ import annotations

import base64
import logging
from pathlib import Path
from uuid import uuid4

from app.config import Settings
from app.models import ContentFormat, GeneratedContent

logger = logging.getLogger(__name__)

# ── Subject-specific visual context ───────────────────────────────────────────

_SUBJECT_VISUAL_STYLE: dict[str, str] = {
    "anatomy": (
        "detailed anatomical cross-section illustration, medical textbook style, "
        "labelled structures, clean white background, high-contrast line art with "
        "colour-coded tissue layers"
    ),
    "physiology": (
        "physiology diagram with accurate graph axes, schematic representation of "
        "physiological process, clean educational infographic style"
    ),
    "biochemistry": (
        "metabolic pathway diagram, enzyme-substrate interaction schematic, "
        "colour-coded molecules, clear arrows showing reaction direction, "
        "textbook biochemistry illustration style"
    ),
    "pathology": (
        "histopathology-inspired educational schematic showing cellular architecture, "
        "microscopy-style circular field of view, labelled pathological features, "
        "H&E stain colour palette (pink cytoplasm, purple nuclei)"
    ),
    "pharmacology": (
        "drug mechanism of action diagram, receptor-ligand interaction schematic, "
        "dose-response curve illustration, molecular pharmacology educational style"
    ),
    "microbiology": (
        "microbiology educational diagram, Gram stain or Ziehl-Neelsen stain "
        "representation, microscopy field schematic with labelled micro-organisms, "
        "clinical microbiology textbook style"
    ),
    "forensic_medicine": (
        "forensic medicine educational schematic, body chart or autopsy diagram style, "
        "clinical forensic illustration, no graphic content, educational context only"
    ),
    "community_medicine": (
        "public health infographic, epidemiology diagram, 2×2 contingency table "
        "or flow chart for screening, clean data visualisation style"
    ),
    "general_medicine": (
        "clinical medicine educational schematic — ECG trace, chest auscultation "
        "diagram, or clinical sign illustration; medical textbook style"
    ),
    "general_surgery": (
        "surgical anatomy educational illustration, operative diagram, "
        "schematic X-ray or CT finding, clean clinical illustration style"
    ),
    "obstetrics_gynecology": (
        "obstetrics educational schematic — partograph, fetal lie/presentation "
        "diagram, or gynaecology anatomy cross-section, medical textbook style"
    ),
    "pediatrics": (
        "paediatrics educational illustration — growth chart, clinical assessment "
        "schematic, or developmental milestone diagram, friendly medical style"
    ),
    "ophthalmology": (
        "ophthalmology educational diagram — fundus schematic, eye cross-section, "
        "or visual field defect map, clinical ophthalmology illustration style"
    ),
    "ent": (
        "ENT educational diagram — tympanic membrane view, sinonasal anatomy, "
        "or audiogram schematic, otolaryngology textbook illustration style"
    ),
    "orthopedics": (
        "orthopaedics educational diagram — joint anatomy, fracture classification "
        "schematic, or X-ray pattern illustration, clean clinical style"
    ),
    "dermatology": (
        "dermatology educational illustration — skin lesion morphology diagram, "
        "skin cross-section with labelled layers, or dermatoscopy pattern schematic"
    ),
    "psychiatry": (
        "psychiatry educational schematic — brain diagram with labelled regions, "
        "neurotransmitter pathway illustration, or clinical assessment flow chart"
    ),
    "radiology": (
        "radiology educational schematic — chest X-ray or CT cross-section diagram "
        "with labelled findings, clean black-and-white X-ray illustration style"
    ),
    "anesthesiology": (
        "anaesthesiology educational diagram — airway anatomy cross-section, "
        "Mallampati classification illustration, or anaesthetic circuit schematic"
    ),
}

_FORMAT_VISUAL_GUIDANCE: dict[str, str] = {
    "mcq": "clinical vignette image, single dominant diagnostic clue clearly visible",
    "image_based_question": (
        "high-detail diagnostic image, single most important pathological or anatomical finding "
        "prominently centred, supporting structures visible for context"
    ),
    "rapid_revision": "clean summary diagram, key concept illustrated with labelled components",
    "concise_notes": "educational summary card style, key points illustrated with icons or diagrams",
    "clinical_case": "clinical scenario illustration, patient-centred schematic showing presenting signs",
    "pyq_concept": "NEET-PG frequently tested concept illustrated, exam-pattern visual",
    "flashcard": "simple clear illustration, one dominant concept, minimal background clutter",
    "mnemonic": "visual mnemonic aid, colour-coded components, memorable diagram layout",
    "true_false": "clear factual illustration of the stated concept for visual confirmation",
    "one_liner_recall": "minimal focused diagram highlighting the single fact to recall",
    "practical_viva": "examination finding schematic, demonstrating the clinical sign clearly",
}

# ── Prompt builder ─────────────────────────────────────────────────────────────

class MedicalImageGenerator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def configured(self) -> bool:
        return bool(self.settings.generate_realistic_images and self.settings.openai_api_key)

    async def create_visual(self, content: GeneratedContent) -> Path | None:
        if not self.configured:
            return None

        prompt = self._build_prompt(content)
        logger.debug("Image prompt: %s", prompt[:300])

        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=self.settings.openai_api_key)

        try:
            response = await client.images.generate(
                model=self.settings.openai_image_model,
                prompt=prompt,
                size=self.settings.openai_image_size,
                quality=self.settings.openai_image_quality,
                n=1,
            )
        except Exception as exc:
            logger.warning("Image generation API call failed: %s", exc)
            return None

        image_data = response.data[0].b64_json if response.data else None
        if not image_data:
            logger.warning("Image generation returned no base64 payload.")
            return None

        path = self.settings.generated_dir / f"visual_{_subject_key(content)}_{uuid4().hex[:8]}.png"
        path.write_bytes(base64.b64decode(image_data))
        logger.info("AI medical visual generated: %s", path)
        return path

    def _build_prompt(self, content: GeneratedContent) -> str:
        subj_key = _subject_key(content)
        fmt_key = content.content_format.value

        subject_style = _SUBJECT_VISUAL_STYLE.get(subj_key, "medical education illustration, clean style")
        format_guidance = _FORMAT_VISUAL_GUIDANCE.get(fmt_key, "clear educational medical diagram")

        topic = content.poster_text or content.title or subj_key.replace("_", " ")
        visual_desc = content.visual_description or ""
        labels = ", ".join((content.visual_labels or content.image_based_data or [])[:4])

        subject_display = subj_key.replace("_", " ").title()

        # Core accuracy instructions
        accuracy_block = (
            "ACCURACY REQUIREMENTS: "
            "Anatomy must be correct — correct number of structures, correct relative positions. "
            "If showing an ECG, the PQRST morphology must be physiologically plausible. "
            "If showing a histology field, cell morphology must match the stated diagnosis. "
            "If showing an X-ray pattern, density and distribution must be radiologically plausible. "
            "No fantasy anatomy. No placeholder shapes instead of real structures."
        )

        # Style/quality instructions
        style_block = (
            "STYLE: Clean, high-contrast, professional medical education illustration. "
            "White or very light background. Precise line art with accurate proportions. "
            "Colour used purposefully: highlight the key diagnostic feature in a contrasting colour. "
            "Text labels if present must be in English, legible, and correctly spelled. "
            "No watermarks, no logos, no copyright symbols, no branded content. "
            "Resolution: sharp at 1024×1024. No blurring, no painting effects — schematic clarity."
        )

        # Safety instructions
        safety_block = (
            "IMPORTANT: This is for educational purposes only. "
            "Do not include identifiable patient photographs. "
            "Do not reproduce any copyrighted figure or branded courseware. "
            "Use original schematic / diagram style only."
        )

        prompt = (
            f"Create a medical education illustration for {subject_display}: {topic}. "
            f"Visual style: {subject_style}. "
            f"Content format requirement: {format_guidance}. "
        )

        if visual_desc:
            prompt += f"Specific visual: {visual_desc}. "

        if labels:
            prompt += (
                f"The image must clearly show these labelled features: {labels}. "
                "Each label should be visually distinct and identifiable. "
            )

        prompt += f"{accuracy_block} {style_block} {safety_block}"
        return prompt[:4000]  # OpenAI prompt limit


def _subject_key(content: GeneratedContent) -> str:
    if content.subject:
        return content.subject.value
    if content.news_topic:
        return content.news_topic.value
    return "general_medicine"
