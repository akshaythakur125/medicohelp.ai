import json
import logging
import random
from typing import Any

import httpx

from app.config import Settings
from app.models import ContentCategory, ContentFormat, GeneratedContent, PostLane, Subject

logger = logging.getLogger(__name__)


class AIContentClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def generate(self, subject: Subject, content_format: ContentFormat) -> GeneratedContent:
        # AI path: only when a provider + key are both configured
        if self._ai_configured():
            prompt = self._build_prompt(subject, content_format)
            try:
                return await self._dispatch_ai(prompt, subject, content_format)
            except Exception as exc:
                logger.warning("AI generation failed, falling back to library: %s", exc)

        # Library path: always available, no API key required
        return self._serve_from_library(subject, content_format)

    # ── AI dispatch ────────────────────────────────────────────────────────────

    def _ai_configured(self) -> bool:
        p = self.settings.ai_provider
        return (
            (p == "anthropic" and bool(self.settings.anthropic_api_key))
            or (p == "openai" and bool(self.settings.openai_api_key))
            or (p == "gemini" and bool(self.settings.gemini_api_key))
        )

    async def _dispatch_ai(
        self,
        prompt: str,
        subject: Subject,
        content_format: ContentFormat,
    ) -> GeneratedContent:
        p = self.settings.ai_provider
        if p == "anthropic":
            return await self._generate_with_anthropic(prompt, subject, content_format)
        if p == "openai":
            return await self._generate_with_openai(prompt, subject, content_format)
        if p == "gemini":
            return await self._generate_with_gemini(prompt, subject, content_format)
        raise RuntimeError(f"Unknown ai_provider: {p}")

    def _build_prompt(self, subject: Subject, content_format: ContentFormat) -> str:
        template_path = self.settings.prompts_dir / f"{content_format.value}.md"
        base_template = self.settings.prompts_dir / "base.md"

        base = base_template.read_text(encoding="utf-8") if base_template.exists() else ""
        detail = template_path.read_text(encoding="utf-8") if template_path.exists() else ""
        return (
            f"{base}\n\n"
            f"Subject: {subject.value}\n"
            f"Content format: {content_format.value}\n\n"
            f"{detail}"
        ).strip()

    async def _generate_with_anthropic(
        self,
        prompt: str,
        subject: Subject,
        content_format: ContentFormat,
    ) -> GeneratedContent:
        import anthropic

        model = self.settings.ai_model
        if not model.startswith("claude"):
            model = "claude-haiku-4-5-20251001"

        client = anthropic.AsyncAnthropic(api_key=self.settings.anthropic_api_key)
        system = (
            "You are an expert MBBS and NEET PG medical educator. "
            "Produce accurate, concise, exam-oriented undergraduate medical teaching content. "
            "Respond ONLY with valid JSON — no markdown fences, no extra text. "
            "Start your response with { and end with }."
        )
        message = await client.messages.create(
            model=model,
            max_tokens=1500,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text
        return self._parse_content(raw, subject, content_format)

    async def _generate_with_openai(
        self,
        prompt: str,
        subject: Subject,
        content_format: ContentFormat,
    ) -> GeneratedContent:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        response = await client.chat.completions.create(
            model=self.settings.ai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert MBBS and NEET PG medical educator. Produce accurate, concise, "
                        "exam-oriented undergraduate medical teaching content."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        raw = response.choices[0].message.content or "{}"
        return self._parse_content(raw, subject, content_format)

    async def _generate_with_gemini(
        self,
        prompt: str,
        subject: Subject,
        content_format: ContentFormat,
    ) -> GeneratedContent:
        model = self.settings.ai_model if self.settings.ai_model.startswith("gemini") else "gemini-1.5-flash"
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent?key={self.settings.gemini_api_key}"
        )
        payload: dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "responseMimeType": "application/json",
            },
        }
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
        data = response.json()
        raw = data["candidates"][0]["content"]["parts"][0]["text"]
        return self._parse_content(raw, subject, content_format)

    def _parse_content(self, raw: str, subject: Subject, content_format: ContentFormat) -> GeneratedContent:
        try:
            payload = json.loads(raw)
            payload["subject"] = subject
            payload["content_format"] = content_format
            if isinstance(payload.get("hashtags"), str):
                payload["hashtags"] = [tag.strip() for tag in payload["hashtags"].split() if tag.strip()]
            if isinstance(payload.get("image_based_data"), str):
                payload["image_based_data"] = [payload["image_based_data"]]
            return GeneratedContent.model_validate(payload)
        except Exception as exc:
            logger.exception("AI response parsing failed: %s", raw[:500])
            raise ValueError("AI provider returned invalid content JSON.") from exc

    # ── Library path (offline, no API key required) ────────────────────────────

    def _serve_from_library(self, subject: Subject, content_format: ContentFormat) -> GeneratedContent:
        # 1. SmartContentEngine: spaced repetition + format variation
        try:
            from app.services.content_engine import SmartContentEngine
            engine = SmartContentEngine(self.settings)
            content = engine.generate(subject, content_format)
            if content:
                logger.info("SmartContentEngine served: %s", content.title)
                return content
        except Exception as exc:
            logger.debug("SmartContentEngine unavailable: %s", exc)

        # 2. Raw library: direct lookup with format fallback
        try:
            from content.loader import get_library
            content = get_library().get(subject, content_format)
            if content:
                logger.info("Library served: %s / %s", subject.value, content_format.value)
                return content
        except Exception as exc:
            logger.debug("Content library unavailable: %s", exc)

        # 3. Procedural fallback: built-in subject-specific content
        logger.info("Using procedural fallback for %s / %s", subject.value, content_format.value)
        return self._procedural_fallback(subject, content_format)

    def _procedural_fallback(self, subject: Subject, content_format: ContentFormat) -> GeneratedContent:
        display_subject = subject.value.replace("_", " ").title()
        display_format = content_format.value.replace("_", " ").title()
        high_yield_topics = {
            Subject.anatomy: "Erb palsy from upper trunk brachial plexus injury",
            Subject.physiology: "right shift of the oxygen dissociation curve",
            Subject.biochemistry: "classic urea cycle block pattern",
            Subject.pathology: "caseating granuloma suggestive of tuberculosis",
            Subject.pharmacology: "beta-blocker risk in bronchial asthma",
            Subject.microbiology: "acid-fast bacilli on Ziehl-Neelsen stain",
            Subject.forensic_medicine: "fixed postmortem lividity and body position",
            Subject.community_medicine: "screening test interpretation using a 2x2 table",
            Subject.general_medicine: "hyperkalemia on ECG with tall tented T waves",
            Subject.general_surgery: "pneumoperitoneum with air under diaphragm",
            Subject.obstetrics_gynecology: "prolonged labor on partograph crossing action line",
            Subject.pediatrics: "severe dehydration using clinical sign panel",
            Subject.ophthalmology: "central retinal artery occlusion with cherry-red spot",
            Subject.ent: "conductive hearing loss on Rinne and Weber tests",
            Subject.orthopedics: "supracondylar fracture with brachial artery risk",
            Subject.dermatology: "erythema multiforme target lesions",
            Subject.psychiatry: "schizophrenia symptom cluster with first-rank symptoms",
            Subject.radiology: "pneumoperitoneum with air under diaphragm on erect X-ray",
            Subject.anesthesiology: "difficult airway predicted by Mallampati and mouth opening",
        }
        topic = high_yield_topics.get(subject, "high-yield clinical concept")
        visual_map = {
            Subject.anatomy: ("Labelled nerve plexus diagram with lesion site highlighted", ["Roots", "Trunks", "Cords", "Deficit"]),
            Subject.physiology: ("Oxygen dissociation curve with left and right shifts", ["Left shift", "Right shift", "P50", "Hb saturation"]),
            Subject.biochemistry: ("Metabolic pathway block diagram with accumulated metabolite", ["Enzyme block", "Substrate", "Product", "Toxic metabolite"]),
            Subject.pathology: ("Microscopy-style granuloma schematic with central necrosis", ["Epithelioid cells", "Giant cell", "Caseation", "Lymphocytes"]),
            Subject.pharmacology: ("Drug receptor flow diagram with contraindication warning", ["Drug class", "Receptor", "Effect", "Avoid in"]),
            Subject.microbiology: ("Stain-field schematic showing acid-fast bacilli", ["Red bacilli", "Blue background", "Ziehl-Neelsen", "TB clue"]),
            Subject.forensic_medicine: ("Body-position diagram showing postmortem lividity distribution", ["Dependent area", "Blanching", "Fixation", "Time clue"]),
            Subject.community_medicine: ("Screening 2x2 table and ROC-style curve", ["Sensitivity", "Specificity", "False negative", "Cutoff"]),
            Subject.general_medicine: ("ECG strip schematic with tall tented T waves", ["Tall T wave", "QRS widening", "PR change", "Hyperkalemia"]),
            Subject.general_surgery: ("Erect X-ray abdomen style schematic with free gas clue", ["Free air", "Diaphragm", "Bowel gas", "Perforation"]),
            Subject.obstetrics_gynecology: ("Partograph chart with alert and action lines", ["Alert line", "Action line", "Cervical dilatation", "Delay"]),
            Subject.pediatrics: ("Clinical signs panel for dehydration severity", ["Sunken eyes", "Skin pinch", "Thirst", "Lethargy"]),
            Subject.ophthalmology: ("Fundus schematic with cherry-red spot", ["Pale retina", "Cherry-red spot", "Macula", "CRAO"]),
            Subject.ent: ("Tuning fork test diagram near ear and forehead", ["Rinne", "Weber", "Air conduction", "Bone conduction"]),
            Subject.orthopedics: ("Elbow fracture schematic with neurovascular warning", ["Distal humerus", "Brachial artery", "Median nerve", "Volkmann risk"]),
            Subject.dermatology: ("Target lesion skin schematic with concentric rings", ["Dusky center", "Pale ring", "Erythematous rim", "Target lesion"]),
            Subject.psychiatry: ("Symptom cluster mind-map for schizophrenia", ["Thought echo", "Voices", "Passivity", "Delusion"]),
            Subject.radiology: ("Chest/abdomen X-ray schematic with highlighted sign", ["Lucency", "Diaphragm", "Air crescent", "Emergency clue"]),
            Subject.anesthesiology: ("Airway assessment panel with warning markers", ["Mallampati", "Mouth opening", "Neck mobility", "Jaw protrusion"]),
        }
        visual_description, visual_labels = visual_map.get(
            subject,
            ("Labelled educational schematic with the dominant exam clue highlighted", ["Key clue", "Location", "Diagnosis", "Trap"]),
        )
        stems = {
            ContentFormat.mcq: (
                f"A clinical vignette points to {topic}. Interpret the key clue and choose the best answer.",
                f"Answer with reasoning: Identify the key clue for {topic}, eliminate distractors, and revise the tested concept.",
            ),
            ContentFormat.image_based_question: (
                f"Image-based question: interpret the visual clue for {topic}.",
                f"Image data: Look for the dominant pattern, location, symmetry, and one negative clue before choosing the answer.",
            ),
            ContentFormat.concise_notes: (
                f"Notes: {topic} in 5 exam-ready points.",
                f"Concise notes: Definition, key mechanism, clinical clue, investigation, and common exam trap for {topic}.",
            ),
            ContentFormat.clinical_case: (
                f"Case challenge: Patient presentation suggests {topic}. What is the next step?",
                f"Clinical reasoning: Start from the presenting clue, classify severity, choose the safest next step, and remember the red flag.",
            ),
            ContentFormat.rapid_revision: (
                f"Rapid revision: {topic}. One clue, one trap, one takeaway.",
                f"Rapid revision: The exam usually tests the signature clue, the confusing differential, and the management/investigation pearl.",
            ),
            ContentFormat.practical_viva: (
                f"Practical viva: How will you identify and explain {topic}?",
                f"Viva answer framework: Identify the finding, name the diagnosis/concept, explain mechanism, and mention one clinical relevance.",
            ),
            ContentFormat.pyq_concept: (
                f"PYQ-style concept: recognize the recurring exam pattern for {topic}.",
                f"Previous-year pattern: This concept is repeatedly tested through one key clue, one close mimic, and one management or mechanism trap.",
            ),
        }
        poster_text, caption_tail = stems.get(content_format, random.choice(list(stems.values())))
        long_question = (
            f"An MBBS student is shown a realistic {display_subject.lower()} image in an exam setting.\n"
            f"The visual shows a high-yield pattern of {topic}.\n"
            f"The most important clue is '{visual_labels[0]}', seen in relation to '{visual_labels[1]}'.\n"
            "The patient vignette is intentionally short because the image carries the diagnostic weight.\n"
            f"A close mimic may look similar, but it would not show '{visual_labels[2]}' in this pattern.\n"
            "Use the labelled findings before reading the answer choices.\n"
            "Which option is the most relevant diagnosis or concept?"
        )
        explanation = (
            f"The correct answer is {topic.title()} because the visual pattern is anchored by {visual_labels[0]} "
            f"and its relationship to {visual_labels[1]}. In image-based questions, the safest approach is to first "
            "name the structure or abnormal pattern, then connect it to the clinical setting, and only then compare "
            "the distractors. The closest mimic is tempting because it shares a superficial appearance, but it does "
            f"not explain the key labelled clue: {visual_labels[2]}."
        )
        lane_map = {
            ContentFormat.image_based_question: PostLane.image_based,
            ContentFormat.pyq_concept: PostLane.pyq_concept,
            ContentFormat.rapid_revision: PostLane.quick_revision,
        }
        return GeneratedContent(
            title=f"{display_subject}: {display_format}",
            caption=(
                f"{display_subject} {display_format}\n\n"
                f"Topic: {topic.title()}.\n\n"
                f"{caption_tail}\n\n"
                "Answer: A. Most likely exam diagnosis/concept.\n\n"
                "Use this as educational revision content, not patient-specific medical advice."
            ),
            hashtags=[
                "#MedicoHelp",
                f"#{display_subject.replace(' ', '')}",
                "#MBBS",
                "#NEETPG",
                "#MedicalEducation",
            ],
            poster_text=poster_text,
            image_prompt=(
                f"Create a clean educational medical visual for {display_subject}: {topic}, "
                "with labeled high-yield visual clues."
            ),
            visual_description=visual_description,
            visual_labels=visual_labels,
            question=long_question,
            options=[
                f"A. {topic.title()}",
                "B. Closely related distractor",
                "C. Common but less likely alternative",
                "D. Unrelated exam trap",
            ],
            correct_answer=f"A. {topic.title()}",
            explanation=explanation,
            high_yield_takeaway=f"Spot the key visual clue first; it usually unlocks {topic}.",
            relevance_rationale=(
                f"{topic.title()} is high-yield in {display_subject} because it is commonly tested through a "
                "recognizable visual pattern and a short clinical stem."
            ),
            image_answerability=(
                f"The image is essential because {visual_labels[0]}, {visual_labels[1]}, and {visual_labels[2]} "
                f"directly point to {topic} and separate it from close mimics."
            ),
            image_based_data=[
                visual_labels[0],
                visual_labels[1],
                visual_labels[2],
                visual_labels[3],
            ],
            subject=subject,
            post_lane=lane_map.get(content_format),
            content_format=content_format,
        )


def legacy_category_to_subject_format(category: ContentCategory) -> tuple[Subject, ContentFormat]:
    mapping = {
        ContentCategory.neet_pg_mcq: (Subject.ophthalmology, ContentFormat.mcq),
        ContentCategory.clinical_case: (Subject.ophthalmology, ContentFormat.clinical_case),
        ContentCategory.retina_quiz: (Subject.ophthalmology, ContentFormat.image_based_question),
        ContentCategory.cataract_pearl: (Subject.ophthalmology, ContentFormat.concise_notes),
        ContentCategory.glaucoma_fact: (Subject.ophthalmology, ContentFormat.rapid_revision),
        ContentCategory.emergency_ophthalmology: (Subject.ophthalmology, ContentFormat.clinical_case),
    }
    return mapping[category]
