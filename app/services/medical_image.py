import base64
import logging
from pathlib import Path
from uuid import uuid4

from openai import AsyncOpenAI

from app.config import Settings
from app.models import GeneratedContent

logger = logging.getLogger(__name__)


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
        client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        response = await client.images.generate(
            model=self.settings.openai_image_model,
            prompt=prompt,
            size=self.settings.openai_image_size,
            quality=self.settings.openai_image_quality,
            n=1,
        )

        image_data = response.data[0].b64_json
        if not image_data:
            logger.warning("Image generation returned no base64 payload.")
            return None

        path = self.settings.generated_dir / f"visual_{content.subject.value}_{uuid4().hex[:8]}.png"
        path.write_bytes(base64.b64decode(image_data))
        logger.info("Realistic medical visual generated: %s", path)
        return path

    def _build_prompt(self, content: GeneratedContent) -> str:
        labels = ", ".join(content.visual_labels or content.image_based_data)
        return (
            "Create an original realistic medical education image for an MBBS/NEET PG image-based question. "
            "Do not copy any coaching app, textbook figure, branded slide, question bank screenshot, watermark, "
            "or real patient-identifying image. Use a realistic but educational style suitable for a teaching card. "
            f"Subject/topic: {self._scope(content)}. "
            f"Topic: {content.poster_text}. "
            f"Visual description: {content.visual_description or content.image_prompt or content.poster_text}. "
            f"Important visual labels/clues: {labels}. "
            "Keep the image clean, medically plausible, high contrast, and without large text blocks."
        )

    def _scope(self, content: GeneratedContent) -> str:
        if content.subject:
            return content.subject.value.replace("_", " ")
        if content.news_topic:
            return content.news_topic.value.replace("_", " ")
        return "medical education"
