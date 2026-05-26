import logging
import random
from pathlib import Path
from typing import Any

from app.config import Settings
from app.models import (
    ContentCategory,
    ContentFormat,
    Difficulty,
    GeneratedContent,
    GenerateResponse,
    NewsItem,
    NewsTopic,
    PostLane,
    SlotType,
    Subject,
)
from app.services.ai_client import AIContentClient, legacy_category_to_subject_format
from app.services.analytics import ContentAnalytics
from app.services.content_engine import SmartContentEngine
from app.services.content_strategy import ContentStrategy
from app.services.enrichment import enrich_for_engagement
from app.services.formatter import format_for_telegram
from app.services.medical_image import MedicalImageGenerator
from app.services.news import NewsSweeper
from app.services.poster import PosterGenerator
from app.services.quality import ContentQualityGate
from app.services.retry_queue import RetryQueue
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
        self._engine = SmartContentEngine(settings)
        self._analytics = ContentAnalytics(settings.logs_dir)
        self._retry_queue = RetryQueue(settings.logs_dir)
        self._paused = False

        self.content_strategy.set_weak_provider(self._get_weak_list)

    # ── Public API ───────────────────────────────────────────────────────

    @property
    def paused(self) -> bool:
        return self._paused

    def pause(self) -> None:
        self._paused = True
        logger.info("Posting paused by admin.")

    def resume(self) -> None:
        self._paused = False
        logger.info("Posting resumed by admin.")

    async def generate_post(
        self,
        subject: Subject | None = None,
        content_format: ContentFormat | None = None,
        category: ContentCategory | None = None,
        publish_to_telegram: bool = True,
        difficulty: Difficulty | None = None,
    ) -> GenerateResponse:
        if category and not subject and not content_format:
            subject, content_format = legacy_category_to_subject_format(category)

        selected_subject = subject or random.choice(list(Subject))
        selected_format = content_format or random.choice(list(ContentFormat))
        try:
            content = await self.ai_client.generate(selected_subject, selected_format)
            if category:
                content.category = category
            if difficulty:
                content.difficulty = difficulty.value
            self.quality_gate.validate(content)
            content = enrich_for_engagement(content)

            poster_path: Path = Path("text-only")
            if not self.settings.text_only_mode:
                visual_path = None
                try:
                    visual_path = await self.medical_image_generator.create_visual(content)
                except Exception as exc:
                    await self.store.save_error(
                        "Image generation failed; using fallback schematic", {"error": str(exc)}
                    )
                poster_path = self.poster_generator.create(content, visual_image_path=visual_path)

            telegram_posted = False
            if publish_to_telegram:
                if self.settings.text_only_mode:
                    text = format_for_telegram(content)
                    telegram_posted = await self.telegram.send_message(text)
                else:
                    caption = self._build_caption(content.caption, content.hashtags)
                    telegram_posted = await self.telegram.send_photo(poster_path, caption)

            self._record_post(content, telegram_posted)
            return GenerateResponse(
                content=content,
                poster_path=str(poster_path),
                telegram_posted=telegram_posted,
            )
        except Exception as exc:
            await self.store.save_error(
                "Post generation pipeline failed",
                {
                    "error": str(exc),
                    "subject": str(selected_subject),
                    "content_format": str(selected_format),
                    "category": str(category) if category else None,
                },
            )
            logger.warning("Primary generation failed — attempting library fallback: %s", exc)
            fallback = self._library_fallback(selected_subject)
            if fallback:
                telegram_posted = False
                if publish_to_telegram and self.settings.text_only_mode:
                    text = format_for_telegram(fallback)
                    telegram_posted = await self.telegram.send_message(text)
                self._record_post(fallback, telegram_posted)
                return GenerateResponse(
                    content=fallback,
                    poster_path="text-only",
                    telegram_posted=telegram_posted,
                )
            raise

    def _record_post(self, content: GeneratedContent, telegram_posted: bool) -> None:
        self.content_strategy.mark_posted(content.title)
        self._engine.record_performance(
            title=content.title,
            correct=telegram_posted,
            subject=content.subject,
        )
        self._analytics.record_post(content)

    # ── Helpers ──────────────────────────────────────────────────────────

    def _library_fallback(self, subject: Subject | None = None) -> GeneratedContent | None:
        try:
            from content.loader import get_library
            lib = get_library()
            items = lib.pool(subject, ContentFormat.rapid_revision)
            if items:
                return random.choice(items)
            items = lib.pool(None, None)
            if items:
                return random.choice(items)
        except Exception as exc:
            logger.error("Library fallback also failed: %s", exc)
        return None

    def _get_weak_list(self) -> list[dict]:
        return self._engine.weak_topics(threshold=0.6, min_attempts=1)

    def _build_caption(self, caption: str, hashtags: list[str]) -> str:
        normalized_tags = [tag if tag.startswith("#") else f"#{tag}" for tag in hashtags]
        return f"{caption.strip()}\n\n{' '.join(normalized_tags)}".strip()

    # ── News ─────────────────────────────────────────────────────────────

    async def fetch_latest_news(self, topic: NewsTopic) -> list[NewsItem]:
        if topic == NewsTopic.residency:
            return []
        return await self.news_sweeper.fetch_latest(topic)

    async def generate_news_post(
        self, topic: NewsTopic, publish_to_telegram: bool = False
    ) -> GenerateResponse:
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

            await self.store.save_post(content, poster_path, telegram_posted)
            return GenerateResponse(
                content=content, poster_path=str(poster_path), telegram_posted=telegram_posted
            )
        except Exception as exc:
            await self.store.save_error(
                "News/residency post generation failed", {"error": str(exc), "topic": topic}
            )
            raise

    # ── Planned post (called by scheduler) ───────────────────────────────

    async def generate_planned_post(
        self,
        publish_to_telegram: bool = True,
        subject_override: Subject | None = None,
        slot_type: SlotType | None = None,
    ) -> GenerateResponse:
        if self._paused and publish_to_telegram:
            logger.info("Posting is paused — skipping scheduled post.")
            raise RuntimeError("Posting is paused by admin. Use /resume to enable.")

        planned = self.content_strategy.next_post(slot_type=slot_type)

        if planned.news_topic and not subject_override:
            return await self.generate_news_post(
                planned.news_topic, publish_to_telegram=publish_to_telegram
            )

        if planned.lane == PostLane.poll_quiz and not subject_override:
            return await self.generate_poll_post(
                subject=planned.subject,
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        if planned.lane == PostLane.mcq_variant and not subject_override:
            return await self.generate_mcq_variant_post(
                subject=planned.subject,
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        if planned.lane == PostLane.weak_topic_recall and not subject_override:
            return await self.generate_weak_topic_post(
                publish_to_telegram=publish_to_telegram,
            )

        if planned.lane == PostLane.daily_pack and not subject_override:
            return await self.generate_daily_pack_post(
                publish_to_telegram=publish_to_telegram,
            )

        if planned.lane == PostLane.flashcard and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="flashcard",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        if planned.lane == PostLane.mnemonic and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="mnemonic",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        if planned.lane == PostLane.true_false and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="true_false",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        if planned.lane == PostLane.one_liner_recall and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="one_liner",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        return await self.generate_post(
            subject=subject_override or planned.subject,
            content_format=planned.content_format,
            publish_to_telegram=publish_to_telegram,
        )

    # ── Lane generators ──────────────────────────────────────────────────

    async def generate_poll_post(
        self,
        subject: Subject | None = None,
        publish_to_telegram: bool = True,
        difficulty: Difficulty | None = None,
    ) -> GenerateResponse:
        selected_subject = subject or random.choice(list(Subject))
        content = self._engine.generate_variate_mcq(selected_subject)
        if not content:
            content = await self.ai_client.generate(selected_subject, ContentFormat.mcq)

        if difficulty:
            content.difficulty = difficulty.value
        self.quality_gate.validate(content)
        content = enrich_for_engagement(content)

        poster_path = Path("text-only")
        telegram_posted = False

        if publish_to_telegram:
            options = _strip_option_letters(content.options)[:4]
            correct_idx = _correct_option_index(content.options, content.correct_answer or "")
            explanation = (content.high_yield_takeaway or "")[:200]
            if content.explanation and len(explanation) < 50:
                explanation = content.explanation[:200]
            question = (content.question or content.title)[:300]
            telegram_posted = await self.telegram.send_poll(
                question=question,
                options=options,
                correct_option_id=correct_idx,
                explanation=explanation,
            )

        self._record_post(content, telegram_posted)
        return GenerateResponse(
            content=content, poster_path=str(poster_path), telegram_posted=telegram_posted
        )

    async def generate_mcq_variant_post(
        self,
        subject: Subject | None = None,
        publish_to_telegram: bool = True,
        difficulty: Difficulty | None = None,
    ) -> GenerateResponse:
        selected_subject = subject or random.choice(list(Subject))
        content = self._engine.generate_variate_mcq(selected_subject)

        if not content:
            return await self.generate_poll_post(
                subject=selected_subject,
                publish_to_telegram=publish_to_telegram,
                difficulty=difficulty,
            )

        if difficulty:
            content.difficulty = difficulty.value
        self.quality_gate.validate(content)
        content = enrich_for_engagement(content)

        poster_path = Path("text-only")
        telegram_posted = False

        if publish_to_telegram:
            tag = content.difficulty or "medium"
            header = (
                f"🎯 <b>MCQ Variant</b> | {_subj_name(content)} | "
                f"Difficulty: <b>{tag.upper()}</b>\n\n"
            )
            full = header + format_for_telegram(content)
            telegram_posted = await self.telegram.send_message(full)

        self._record_post(content, telegram_posted)
        return GenerateResponse(
            content=content, poster_path=str(poster_path), telegram_posted=telegram_posted
        )

    async def generate_weak_topic_post(
        self,
        publish_to_telegram: bool = True,
    ) -> GenerateResponse:
        weak = self._engine.weak_topics(threshold=0.6, min_attempts=1)
        if not weak:
            return await self.generate_post(publish_to_telegram=publish_to_telegram)

        weakest = weak[0]
        try:
            from content.loader import get_library

            lib = get_library()
            pool = lib.pool(None, None)
            match = [c for c in pool if c.title == weakest["title"]]
            if match:
                source = match[0]
            else:
                subject_val = weakest.get("subject")
                subj = next((s for s in Subject if s.value == subject_val), None)
                if subj:
                    source = lib.get(subj, ContentFormat.rapid_revision)
                else:
                    return await self.generate_post(publish_to_telegram=publish_to_telegram)
        except Exception:
            return await self.generate_post(publish_to_telegram=publish_to_telegram)

        accuracy = weakest.get("accuracy", 0.5)
        attempts = weakest.get("total_attempts", 1)
        header = (
            f"🔁 <b>Weak Topic Recall</b>\n"
            f"Accuracy: {accuracy:.0%} ({attempts} attempts)\n"
            f"Topic: <b>{weakest['title']}</b>\n\n"
        )

        content = source
        poster_path = Path("text-only")
        telegram_posted = False

        if publish_to_telegram:
            body = header + format_for_telegram(content)
            telegram_posted = await self.telegram.send_message(body)

        self._analytics.record_weak_spotlight(
            title=weakest["title"],
            accuracy=weakest.get("accuracy", 0),
            subject=weakest.get("subject"),
        )
        await self.store.save_post(content, poster_path, telegram_posted)
        return GenerateResponse(
            content=content, poster_path=str(poster_path), telegram_posted=telegram_posted
        )

    async def generate_smart_format_post(
        self,
        subject: Subject | None = None,
        smart_format: str = "flashcard",
        publish_to_telegram: bool = True,
        difficulty: Difficulty | None = None,
    ) -> GenerateResponse:
        selected_subject = subject or random.choice(list(Subject))

        content: GeneratedContent | None = None
        if smart_format == "flashcard":
            content = self._engine.generate_flashcard(selected_subject)
        elif smart_format == "mnemonic":
            content = self._engine.generate(selected_subject, ContentFormat.mnemonic)
        elif smart_format == "true_false":
            content = self._engine.generate_true_false(selected_subject)
        elif smart_format == "one_liner":
            content = self._engine.generate_one_liner(selected_subject)

        if not content:
            content = await self.ai_client.generate(
                selected_subject, ContentFormat.rapid_revision
            )

        if difficulty:
            content.difficulty = difficulty.value
        self.quality_gate.validate(content)
        content = enrich_for_engagement(content)

        poster_path = Path("text-only")
        telegram_posted = False
        if publish_to_telegram and self.settings.text_only_mode:
            text = format_for_telegram(content)
            telegram_posted = await self.telegram.send_message(text)

        self._record_post(content, telegram_posted)
        return GenerateResponse(
            content=content, poster_path=str(poster_path), telegram_posted=telegram_posted
        )

    async def generate_daily_pack_post(
        self, publish_to_telegram: bool = True
    ) -> GenerateResponse:
        pack = self._engine.generate_daily_pack(count=5)

        telegram_posted = False
        if publish_to_telegram and pack:
            header = "📦 <b>Daily Revision Pack</b>\n5 quick questions — one per subject!\n"
            await self.telegram.send_message(header)
            for i, item in enumerate(pack, 1):
                self._record_post(item, telegram_posted=True)
                if item.content_format == ContentFormat.mcq:
                    options = _strip_option_letters(item.options)[:4]
                    correct_idx = _correct_option_index(
                        item.options, item.correct_answer or ""
                    )
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

        if pack:
            await self.store.save_post(pack[0], Path("text-only"), telegram_posted)
            return GenerateResponse(
                content=pack[0], poster_path="text-only", telegram_posted=telegram_posted
            )

        return await self.generate_post(publish_to_telegram=publish_to_telegram)

    async def generate_news_post_text(
        self, topic: NewsTopic, publish_to_telegram: bool = False
    ) -> GenerateResponse:
        result = await self.generate_news_post(topic=topic, publish_to_telegram=False)
        if publish_to_telegram and self.settings.text_only_mode:
            text = format_for_telegram(result.content)
            telegram_posted = await self.telegram.send_message(text)
            await self.store.save_post(result.content, Path("text-only"), telegram_posted)
            return GenerateResponse(
                content=result.content,
                poster_path="text-only",
                telegram_posted=telegram_posted,
            )
        return result

    # ── Stats ────────────────────────────────────────────────────────────

    def get_engine_stats(self) -> dict:
        from app.services.content_engine import SmartContentEngine

        engine_stats = SmartContentEngine(self.settings).stats()
        engine_stats["analytics"] = self._analytics.report()
        return engine_stats

    def get_analytics_report(self) -> dict:
        return self._analytics.report()

    async def process_retry_queue(self) -> None:
        await self._retry_queue.process(self._retry_post)

    async def _retry_post(self, entry: dict) -> None:
        subj_val = entry.get("subject")
        subject = next((s for s in Subject if s.value == subj_val), None) if subj_val else None
        fmt_val = entry.get("format")
        content_format = next((f for f in ContentFormat if f.value == fmt_val), None) if fmt_val else None
        await self.generate_post(
            subject=subject,
            content_format=content_format,
            publish_to_telegram=True,
        )


# ── Module-level helpers ──────────────────────────────────────────────────────


def _strip_option_letters(options: list[str]) -> list[str]:
    cleaned = []
    for opt in options:
        text = opt.strip()
        if len(text) >= 3 and text[1] in ".)" and text[0].upper() in "ABCDEFGH":
            text = text[2:].strip()
        cleaned.append(text[:100])
    return cleaned


def _correct_option_index(options: list[str], correct_answer: str) -> int:
    if not correct_answer or not options:
        return 0
    ca = correct_answer.strip()
    for i, opt in enumerate(options):
        if ca and opt.strip().upper().startswith(ca[0].upper() + "."):
            return i
        if ca and opt.strip().upper().startswith(ca[0].upper() + ")"):
            return i
    for i, opt in enumerate(options):
        if ca.lower() in opt.lower() or opt.lower() in ca.lower():
            return i
    return 0


def _subj_name(content: Any) -> str:
    if content.subject:
        return content.subject.value.replace("_", " ").title()
    if getattr(content, "news_topic", None):
        return content.news_topic.value.replace("_", " ").title()
    return "General"
