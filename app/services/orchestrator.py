import logging
import random

from app.config import Settings
from app.models import ContentCategory, ContentFormat, GenerateResponse, NewsItem, NewsTopic, Subject
from app.services.ai_client import AIContentClient, legacy_category_to_subject_format
from app.services.content_strategy import ContentStrategy
from app.services.medical_image import MedicalImageGenerator
from app.services.news import NewsSweeper
from app.services.poster import PosterGenerator
from app.services.quality import ContentQualityGate
from app.services.storage import PostLogStore
from app.services.telegram import TelegramPoster

logger = logging.getLogger(__name__)


class PostOrchestrator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.ai_client = AIContentClient(settings)
        self.medical_image_generator = MedicalImageGenerator(settings)
        self.news_sweeper = NewsSweeper(settings)
        self.poster_generator = PosterGenerator(settings)
        self.quality_gate = ContentQualityGate()
        self.content_strategy = ContentStrategy()
        self.telegram = TelegramPoster(settings)
        self.store = PostLogStore(settings)

    async def generate_post(
        self,
        subject: Subject | None = None,
        content_format: ContentFormat | None = None,
        category: ContentCategory | None = None,
        publish_to_telegram: bool = True,
    ) -> GenerateResponse:
        if category and not subject and not content_format:
            subject, content_format = legacy_category_to_subject_format(category)

        selected_subject = subject or random.choice(list(Subject))
        selected_format = content_format or random.choice(list(ContentFormat))
        try:
            content = await self.ai_client.generate(selected_subject, selected_format)
            if category:
                content.category = category
            self.quality_gate.validate(content)
            visual_path = None
            try:
                visual_path = await self.medical_image_generator.create_visual(content)
            except Exception as exc:
                self.store.save_error("Realistic image generation failed; using fallback schematic", {"error": str(exc)})
            poster_path = self.poster_generator.create(content, visual_image_path=visual_path)
            telegram_posted = False

            if publish_to_telegram:
                caption = self._build_caption(content.caption, content.hashtags)
                telegram_posted = await self.telegram.send_photo(poster_path, caption)

            self.store.save_post(content, poster_path, telegram_posted)
            return GenerateResponse(
                content=content,
                poster_path=str(poster_path),
                telegram_posted=telegram_posted,
            )
        except Exception as exc:
            self.store.save_error(
                "Post generation pipeline failed",
                {
                    "error": str(exc),
                    "subject": selected_subject,
                    "content_format": selected_format,
                    "category": category,
                },
            )
            raise

    def _build_caption(self, caption: str, hashtags: list[str]) -> str:
        normalized_tags = [tag if tag.startswith("#") else f"#{tag}" for tag in hashtags]
        return f"{caption.strip()}\n\n{' '.join(normalized_tags)}".strip()

    async def fetch_latest_news(self, topic: NewsTopic) -> list[NewsItem]:
        if topic == NewsTopic.residency:
            return []
        return await self.news_sweeper.fetch_latest(topic)

    async def generate_news_post(self, topic: NewsTopic, publish_to_telegram: bool = False) -> GenerateResponse:
        try:
            if topic == NewsTopic.residency:
                content = self.news_sweeper.build_residency_tip()
            else:
                items = await self.news_sweeper.fetch_latest(topic)
                content = self.news_sweeper.build_content(topic, items)

            poster_path = self.poster_generator.create(content)
            telegram_posted = False
            if publish_to_telegram:
                caption = self._build_caption(content.caption, content.hashtags)
                telegram_posted = await self.telegram.send_photo(poster_path, caption)

            self.store.save_post(content, poster_path, telegram_posted)
            return GenerateResponse(content=content, poster_path=str(poster_path), telegram_posted=telegram_posted)
        except Exception as exc:
            self.store.save_error("News/residency post generation failed", {"error": str(exc), "topic": topic})
            raise

    async def generate_planned_post(self, publish_to_telegram: bool = True) -> GenerateResponse:
        planned = self.content_strategy.next_post()
        if planned.news_topic:
            return await self.generate_news_post(planned.news_topic, publish_to_telegram=publish_to_telegram)
        return await self.generate_post(
            subject=planned.subject,
            content_format=planned.content_format,
            publish_to_telegram=publish_to_telegram,
        )
