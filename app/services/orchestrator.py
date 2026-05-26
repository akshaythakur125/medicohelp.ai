import logging
import random
from pathlib import Path

from app.config import Settings
from app.models import ContentCategory, ContentFormat, GeneratedContent, GenerateResponse, NewsItem, NewsTopic, Subject
from app.services.ai_client import AIContentClient, legacy_category_to_subject_format
from app.services.content_strategy import ContentStrategy
from app.services.formatter import format_for_telegram
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

            poster_path: Path = Path("text-only")
            if not self.settings.text_only_mode:
                visual_path = None
                try:
                    visual_path = await self.medical_image_generator.create_visual(content)
                except Exception as exc:
                    self.store.save_error("Image generation failed; using fallback schematic", {"error": str(exc)})
                poster_path = self.poster_generator.create(content, visual_image_path=visual_path)

            telegram_posted = False
            if publish_to_telegram:
                if self.settings.text_only_mode:
                    text = format_for_telegram(content)
                    telegram_posted = await self.telegram.send_message(text)
                else:
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
                    "subject": str(selected_subject),
                    "content_format": str(selected_format),
                    "category": str(category) if category else None,
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

    async def generate_planned_post(
        self,
        publish_to_telegram: bool = True,
        subject_override: Subject | None = None,
    ) -> GenerateResponse:
        from app.models import PostLane
        planned = self.content_strategy.next_post()

        if planned.news_topic and not subject_override:
            return await self.generate_news_post(planned.news_topic, publish_to_telegram=publish_to_telegram)

        if planned.lane == PostLane.poll_quiz and not subject_override:
            return await self.generate_poll_post(
                subject=planned.subject,
                publish_to_telegram=publish_to_telegram,
            )

        if planned.lane == PostLane.daily_pack and not subject_override:
            return await self.generate_daily_pack_post(publish_to_telegram=publish_to_telegram)

        if planned.lane == PostLane.flashcard and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="flashcard",
                publish_to_telegram=publish_to_telegram,
            )

        if planned.lane == PostLane.mnemonic and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="mnemonic",
                publish_to_telegram=publish_to_telegram,
            )

        return await self.generate_post(
            subject=subject_override or planned.subject,
            content_format=planned.content_format,
            publish_to_telegram=publish_to_telegram,
        )

    async def generate_poll_post(
        self,
        subject: Subject | None = None,
        publish_to_telegram: bool = True,
    ) -> GenerateResponse:
        """Generate an MCQ and send it as a native Telegram quiz poll."""
        selected_subject = subject or random.choice(list(Subject))
        content = await self.ai_client.generate(selected_subject, ContentFormat.mcq)
        self.quality_gate.validate(content)

        poster_path = Path("text-only")
        telegram_posted = False

        if publish_to_telegram:
            options = _strip_option_letters(content.options)[:4]
            correct_idx = _correct_option_index(content.options, content.correct_answer or "")
            explanation = (content.high_yield_takeaway or "")[:200]
            question = (content.question or content.title)[:300]
            telegram_posted = await self.telegram.send_poll(
                question=question,
                options=options,
                correct_option_id=correct_idx,
                explanation=explanation,
            )

        self.store.save_post(content, poster_path, telegram_posted)
        return GenerateResponse(content=content, poster_path=str(poster_path), telegram_posted=telegram_posted)

    async def generate_smart_format_post(
        self,
        subject: Subject | None = None,
        smart_format: str = "flashcard",
        publish_to_telegram: bool = True,
    ) -> GenerateResponse:
        """Generate flashcard/mnemonic/true-false/one-liner via SmartContentEngine."""
        from app.services.content_engine import SmartContentEngine
        engine = SmartContentEngine(self.settings)
        selected_subject = subject or random.choice(list(Subject))

        content: GeneratedContent | None = None
        if smart_format == "flashcard":
            content = engine.generate_flashcard(selected_subject)
        elif smart_format == "mnemonic":
            content = engine.generate(selected_subject, ContentFormat.mnemonic)
        elif smart_format == "true_false":
            content = engine.generate_true_false(selected_subject)
        elif smart_format == "one_liner":
            content = engine.generate_one_liner(selected_subject)

        if not content:
            # Fall back to a plain rapid revision
            content = await self.ai_client.generate(selected_subject, ContentFormat.rapid_revision)

        self.quality_gate.validate(content)
        poster_path = Path("text-only")
        telegram_posted = False
        if publish_to_telegram and self.settings.text_only_mode:
            text = format_for_telegram(content)
            telegram_posted = await self.telegram.send_message(text)

        self.store.save_post(content, poster_path, telegram_posted)
        return GenerateResponse(content=content, poster_path=str(poster_path), telegram_posted=telegram_posted)

    async def generate_daily_pack_post(self, publish_to_telegram: bool = True) -> GenerateResponse:
        """Send a burst of 5 revision items as a daily pack."""
        from app.services.content_engine import SmartContentEngine
        engine = SmartContentEngine(self.settings)
        pack = engine.generate_daily_pack(count=5)

        telegram_posted = False
        if publish_to_telegram and pack:
            header = "📦 <b>Daily Revision Pack</b>\n5 quick questions — one per subject!\n"
            await self.telegram.send_message(header)
            for i, item in enumerate(pack, 1):
                if item.content_format == ContentFormat.mcq:
                    options = _strip_option_letters(item.options)[:4]
                    correct_idx = _correct_option_index(item.options, item.correct_answer or "")
                    await self.telegram.send_poll(
                        question=f"({i}/5) {(item.question or item.title)[:295]}",
                        options=options,
                        correct_option_id=correct_idx,
                        explanation=(item.high_yield_takeaway or "")[:200],
                    )
                else:
                    text = format_for_telegram(item)
                    await self.telegram.send_message(text)
            telegram_posted = True

        # Return the first item as the representative response
        if pack:
            self.store.save_post(pack[0], Path("text-only"), telegram_posted)
            return GenerateResponse(content=pack[0], poster_path="text-only", telegram_posted=telegram_posted)

        # Fallback: plain post
        return await self.generate_post(publish_to_telegram=publish_to_telegram)

    async def generate_news_post_text(self, topic: NewsTopic, publish_to_telegram: bool = False) -> GenerateResponse:
        """Like generate_news_post but sends as a text message in text_only_mode."""
        result = await self.generate_news_post(topic=topic, publish_to_telegram=False)
        if publish_to_telegram and self.settings.text_only_mode:
            text = format_for_telegram(result.content)
            telegram_posted = await self.telegram.send_message(text)
            self.store.save_post(result.content, Path("text-only"), telegram_posted)
            return GenerateResponse(
                content=result.content,
                poster_path="text-only",
                telegram_posted=telegram_posted,
            )
        return result


def _strip_option_letters(options: list[str]) -> list[str]:
    """Remove A./B./C./D. letter prefixes for Telegram poll options (max 100 chars each)."""
    cleaned = []
    for opt in options:
        text = opt.strip()
        if len(text) >= 3 and text[1] in ".)" and text[0].upper() in "ABCDEFGH":
            text = text[2:].strip()
        cleaned.append(text[:100])
    return cleaned


def _correct_option_index(options: list[str], correct_answer: str) -> int:
    """Return the 0-based index of the correct option by matching the letter or full text."""
    if not correct_answer or not options:
        return 0
    ca = correct_answer.strip()
    # Match by leading letter: "B. ..." → options[1]
    for i, opt in enumerate(options):
        if ca and opt.strip().upper().startswith(ca[0].upper() + "."):
            return i
        if ca and opt.strip().upper().startswith(ca[0].upper() + ")"):
            return i
    # Match by substring
    for i, opt in enumerate(options):
        if ca.lower() in opt.lower() or opt.lower() in ca.lower():
            return i
    return 0
