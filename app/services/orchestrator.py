import logging
import random
from pathlib import Path
from typing import Any

from app.config import Settings
from app.models import (
    ContentCategory,
    ContentFormat,
    Difficulty,
    EducationMode,
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
from app.services.education_modes import (
    get_mode_description,
    get_mode_subjects,
    select_mode_subject,
)
from app.services.engagement_tracker import EngagementTracker
from app.services.enrichment import enrich_for_engagement
from app.services.formatter import (
    format_battle_leaderboard,
    format_challenge_result,
    format_daily_challenge_intro,
    format_education_mode_announcement,
    format_exam_countdown,
    format_for_telegram,
    format_streak_message,
    format_weekly_battle_intro,
)
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
        self._engagement = EngagementTracker(settings.logs_dir)
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
            visual_path: Path | None = None

            if not self.settings.text_only_mode and self.medical_image_generator.configured:
                try:
                    visual_path = await self.medical_image_generator.create_visual(content)
                except Exception as exc:
                    await self.store.save_error(
                        "Image generation failed; falling back to text", {"error": str(exc)}
                    )
                if visual_path:
                    poster_path = visual_path

            telegram_posted = False
            if publish_to_telegram:
                text = format_for_telegram(content)
                if self.settings.text_only_mode:
                    telegram_posted = await self.telegram.send_message(text)
                elif visual_path:
                    # AI image ready — send illustration + full educational text
                    telegram_posted = await self.telegram.send_visual_post(visual_path, text)
                else:
                    # No image (not configured or failed) — rich text fallback
                    telegram_posted = await self.telegram.send_message(text)

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

    # ── Education Mode ──────────────────────────────────────────────────

    def _get_active_education_mode(self) -> EducationMode:
        mode_name = self.settings.education_mode
        for mode in EducationMode:
            if mode.value == mode_name:
                return mode
        return EducationMode.comprehensive

    def set_education_mode(self, mode_name: str) -> str:
        for mode in EducationMode:
            if mode.value == mode_name:
                self.settings.education_mode = mode.value
                desc = get_mode_description(mode)
                logger.info("Education mode set to %s", mode.value)
                return desc
        return f"Unknown mode: {mode_name}. Available: comprehensive, first_year_mbbs, final_year_revision, neet_pg_revision, inicet_high_yield, emergency_5_min"

    # ── Engagement ──────────────────────────────────────────────────────

    async def generate_daily_challenge(self, publish_to_telegram: bool = True) -> GenerateResponse | None:
        """Generate and optionally publish the daily challenge MCQ."""
        if not self.settings.engagement_enabled:
            return None

        mode = self._get_active_education_mode()
        subjects = list(get_mode_subjects(mode))
        if not subjects:
            subjects = list(Subject)
        subject = random.choice(subjects)

        content = self._engine.generate_variate_mcq(subject)
        if not content:
            content = self._engine.generate(subject, ContentFormat.mcq)
        if not content:
            return None

        content = enrich_for_engagement(content)
        self._engagement.set_daily_challenge(content)
        self._engagement.update_streak()

        telegram_posted = False
        if publish_to_telegram:
            text = format_daily_challenge_intro(content)
            telegram_posted = await self.telegram.send_message(text)

        self._record_post(content, telegram_posted)
        return GenerateResponse(
            content=content, poster_path="text-only", telegram_posted=telegram_posted
        )

    async def announce_streak(self, publish_to_telegram: bool = True) -> bool:
        """Send a streak update message."""
        if not self.settings.engagement_enabled:
            return False
        self._engagement.update_streak()
        if not publish_to_telegram:
            return False
        text = format_streak_message(
            self._engagement.stats.current_streak,
            self._engagement.stats.longest_streak,
        )
        return await self.telegram.send_message(text)

    async def start_weekly_battle(self, publish_to_telegram: bool = True) -> bool:
        """Start a new weekly revision battle."""
        if not self.settings.engagement_enabled:
            return False
        self._engagement.start_weekly_battle()
        if publish_to_telegram:
            text = format_weekly_battle_intro()
            return await self.telegram.send_message(text)
        return False

    async def end_weekly_battle(self, publish_to_telegram: bool = True) -> bool:
        """End the weekly battle and announce results."""
        if not self.settings.engagement_enabled or not self._engagement.stats.weekly_battle_active:
            return False
        leaderboard = self._engagement.end_battle()
        if leaderboard and publish_to_telegram:
            return await self.telegram.send_message(leaderboard)
        return False

    async def send_engagement_summary(self, publish_to_telegram: bool = True) -> bool:
        """Send an engagement summary with stats."""
        if not self.settings.engagement_enabled:
            return False
        stats = self._engagement.stats
        acc = self._engagement.accuracy_pct()
        lines = [
            "📊 <b>Your Engagement Summary</b>\n",
            f"🔥 Current streak: <b>{stats.current_streak} days</b>",
            f"🏆 Longest streak: <b>{stats.longest_streak} days</b>",
            f"📝 Total answered: <b>{stats.total_attempted}</b>",
            f"✅ Correct: <b>{stats.total_correct}</b>",
            f"🎯 Accuracy: <b>{acc:.1f}%</b>",
        ]
        if stats.weekly_battle_active:
            lines.append(f"⚔️ Battle score: <b>{stats.weekly_battle_score} pts</b>")
        text = "\n".join(lines)
        return await self.telegram.send_message(text)

    # ── Weekly Theme ────────────────────────────────────────────────────

    def get_weekly_theme_subject(self) -> Subject:
        """Return this week's themed subject (config override or auto-rotate by ISO week)."""
        override = self.settings.weekly_theme_subject
        if override:
            for s in Subject:
                if s.value == override:
                    return s

        from datetime import date
        week_number = date.today().isocalendar()[1]
        subjects = list(Subject)
        return subjects[week_number % len(subjects)]

    async def generate_weekly_theme_post(self, publish_to_telegram: bool = True) -> GenerateResponse:
        """Post the weekly theme launch announcement."""
        theme_subject = self.get_weekly_theme_subject()
        content = await self.ai_client.generate(theme_subject, ContentFormat.weekly_theme_intro)
        self.quality_gate.validate(content)
        content = enrich_for_engagement(content)

        poster_path = Path("text-only")
        visual_path: Path | None = None
        telegram_posted = False

        if not self.settings.text_only_mode and self.medical_image_generator.configured:
            try:
                visual_path = await self.medical_image_generator.create_visual(content)
            except Exception:
                pass

        if publish_to_telegram:
            text = format_for_telegram(content)
            if visual_path:
                poster_path = visual_path
                telegram_posted = await self.telegram.send_visual_post(visual_path, text)
            else:
                telegram_posted = await self.telegram.send_message(text)

        self._record_post(content, telegram_posted)
        return GenerateResponse(
            content=content, poster_path=str(poster_path), telegram_posted=telegram_posted
        )

    # ── OSCE Station ─────────────────────────────────────────────────────

    async def generate_osce_post(self, publish_to_telegram: bool = True) -> GenerateResponse:
        """Generate and post the OSCE Station of the Week."""
        subject = self.get_weekly_theme_subject()
        content = await self.ai_client.generate(subject, ContentFormat.osce_station)
        self.quality_gate.validate(content)
        content = enrich_for_engagement(content)

        poster_path = Path("text-only")
        telegram_posted = False

        if publish_to_telegram:
            text = format_for_telegram(content)
            telegram_posted = await self.telegram.send_message(text)

        self._record_post(content, telegram_posted)
        return GenerateResponse(
            content=content, poster_path=str(poster_path), telegram_posted=telegram_posted
        )

    # ── Exam Countdown ────────────────────────────────────────────────────

    def get_exam_days_remaining(self) -> int | None:
        """Return days until NEET PG exam, or None if exam_date not configured."""
        if not self.settings.exam_date:
            return None
        try:
            from datetime import date
            exam = date.fromisoformat(self.settings.exam_date)
            delta = (exam - date.today()).days
            return max(0, delta)
        except ValueError:
            return None

    def is_exam_countdown_active(self) -> bool:
        days = self.get_exam_days_remaining()
        return days is not None and 0 <= days <= self.settings.exam_countdown_days

    async def send_exam_countdown(self, publish_to_telegram: bool = True) -> bool:
        """Send daily exam countdown message if within countdown window."""
        days = self.get_exam_days_remaining()
        if days is None:
            return False

        theme_subject = self.get_weekly_theme_subject()
        subject_name = theme_subject.value.replace("_", " ").title()
        text = format_exam_countdown(days, subject_name)
        if publish_to_telegram:
            return await self.telegram.send_message(text)
        return False

    # ── Study Schedule ────────────────────────────────────────────────────

    # 30-day NEET PG study schedule mapping: (start_day, end_day, subject, key_topics)
    _STUDY_PLAN: list[tuple[int, int, str, list[str]]] = [
        (29, 30, "Anatomy", ["Brachial plexus injuries", "Nerve lesions & deficit patterns", "Clinically tested surface markings"]),
        (27, 28, "Physiology", ["Oxygen-haemoglobin dissociation curve", "Cardiac output & Starling's law", "Renal physiology — GFR, tubular functions"]),
        (25, 26, "Biochemistry", ["Enzyme kinetics — Km, Vmax", "Urea cycle defects", "Vitamins: deficiency & toxicity"]),
        (23, 24, "Pathology", ["Granuloma types — TB vs sarcoid vs fungal", "Neoplasia — benign vs malignant features", "Inflammation mediators"]),
        (21, 22, "Pharmacology", ["Autonomic drugs — adrenergic & cholinergic", "Antibiotics — mechanism & resistance", "Cardiac drugs — antiarrhythmics, antihypertensives"]),
        (19, 20, "Microbiology", ["Gram stain & culture patterns", "Zoonoses & vectors", "Antifungals & antivirals"]),
        (18, 18, "Forensic Medicine", ["Postmortem changes — lividity, rigor, putrefaction", "Wounds classification", "Medico-legal autopsies"]),
        (17, 17, "Community Medicine", ["Vaccines & cold chain", "Nutritional deficiency diseases", "Screening tests — sensitivity, specificity"]),
        (15, 16, "General Medicine", ["ECG — arrhythmias, MI patterns", "Endocrinology — diabetes, thyroid, adrenal", "Rheumatology — autoantibodies"]),
        (13, 14, "General Surgery", ["Abdominal X-ray findings", "Hernias — direct vs indirect", "Surgical anatomy of thyroid & breast"]),
        (11, 12, "Obstetrics & Gynecology", ["Partograph interpretation", "APH causes — placenta praevia vs abruption", "PCOS diagnostic criteria"]),
        (9, 10, "Pediatrics", ["Vaccine schedule — NIS & IAP", "Nutritional disorders — PEM classification", "Developmental milestones"]),
        (8, 8, "Ophthalmology", ["Glaucoma — open vs closed angle", "Cataract surgery complications", "Retinal detachment signs"]),
        (7, 7, "ENT", ["Tuning fork tests", "Cholesteatoma features", "CSF rhinorrhoea causes"]),
        (6, 6, "Orthopedics", ["Fracture healing & complications", "Nerve injuries at fracture sites", "Spine anatomy & cord syndromes"]),
        (5, 5, "Dermatology", ["Bullous disorders — pemphigus vs pemphigoid", "Infections — tinea, leprosy", "Psoriasis pathology"]),
        (4, 4, "Psychiatry", ["Schizophrenia first-rank symptoms", "Drug of choice for each disorder", "ICD-10 vs DSM-5 key differences"]),
        (3, 3, "Radiology", ["Chest X-ray systematic reading", "CT patterns — consolidation, ground-glass", "Barium swallow findings"]),
        (2, 2, "Anesthesiology", ["Airway assessment — Mallampati", "MAC values & anaesthetic depth", "Muscle relaxants & reversal"]),
        (1, 1, "High-Yield Revision", ["PYQ pattern analysis — last 5 years", "Rapid revision of all one-liners", "Mock test simulation"]),
    ]

    def get_todays_study_subjects(self) -> tuple[str, list[str]]:
        """Return (subject, topics) for today based on days remaining to exam."""
        days = self.get_exam_days_remaining()
        if days is None or days > 30:
            # No exam set or >30 days: use weekly theme
            subj = self.get_weekly_theme_subject()
            return subj.value.replace("_", " ").title(), []

        for start, end, subject, topics in self._STUDY_PLAN:
            if end >= days >= start:
                return subject, topics

        return "General Revision", ["Review weak topics", "MCQ practice", "Flashcard run"]

    async def generate_study_schedule_post(self, publish_to_telegram: bool = True) -> bool:
        """Post today's structured study plan."""
        days = self.get_exam_days_remaining()
        subject, topics = self.get_todays_study_subjects()

        from app.services.formatter import format_study_schedule_post
        text = format_study_schedule_post(days or 0, subject, topics)
        if publish_to_telegram:
            return await self.telegram.send_message(text)
        return False

    # ── On-Demand AI Query (for bot commands) ────────────────────────────

    async def query_on_demand(
        self,
        query_type: str,
        query_args: str,
        reply_chat_id: str,
    ) -> None:
        """Generate AI content on-demand for a user query and reply to their chat."""
        FORMAT_MAP = {
            "drug": ContentFormat.drug_of_day,
            "compare": ContentFormat.comparison_table,
            "algorithm": ContentFormat.management_algorithm,
            "ddx": ContentFormat.clinical_case,
            "mistake": ContentFormat.common_mistake,
        }
        target_format = FORMAT_MAP.get(query_type, ContentFormat.rapid_revision)

        # Pick best subject from args or fallback to random
        subject = random.choice(list(Subject))
        for s in Subject:
            if s.value.replace("_", " ") in query_args.lower() or s.value in query_args.lower():
                subject = s
                break

        try:
            await self.telegram.send_message_to(reply_chat_id, "⏳ Generating…")
            content = await self.ai_client.generate(subject, target_format)
            from app.services.formatter import format_for_telegram
            text = format_for_telegram(content)
            await self.telegram.send_message_to(reply_chat_id, text)
        except Exception as exc:
            logger.warning("On-demand query failed: %s", exc)
            await self.telegram.send_message_to(
                reply_chat_id, "❌ Could not generate a response. Try again shortly."
            )

    # ── Education Mode Filtering ───────────────────────────────────────

    def _filter_subject_by_mode(self, subject: Subject) -> Subject | None:
        """Return None if the subject is excluded by current education mode."""
        mode = self._get_active_education_mode()
        allowed = get_mode_subjects(mode)
        if mode.value == "comprehensive":
            return subject
        return subject if subject in allowed else None

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

        if self.settings.engagement_enabled:
            self._engagement.update_streak()

        planned = self.content_strategy.next_post(slot_type=slot_type)

        # Filter subject by education mode
        if planned.subject and not subject_override:
            filtered = self._filter_subject_by_mode(planned.subject)
            if filtered is None:
                logger.info(
                    "Subject %s excluded by current education mode — picking random allowed subject",
                    planned.subject,
                )
                mode = self._get_active_education_mode()
                allowed = list(get_mode_subjects(mode))
                if allowed:
                    subject_override = random.choice(allowed)

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

        # Tier 1 lanes
        if planned.lane == PostLane.clinical_correlation and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="clinical_correlation",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        if planned.lane == PostLane.comparison and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="comparison_table",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        if planned.lane == PostLane.management_algo and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="management_algorithm",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        if planned.lane == PostLane.drug_spotlight and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="drug_of_day",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        # Tier 2 lanes
        if planned.lane == PostLane.pimp_round and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="pimp_question",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        if planned.lane == PostLane.spot_diagnosis and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="spot_diagnosis",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        if planned.lane == PostLane.ward_tip and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="ward_tip",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        if planned.lane == PostLane.case_series and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="case_unfolding",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        # Tier 3 lanes
        if planned.lane == PostLane.osce_prep and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="osce_station",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        if planned.lane == PostLane.mistake_corner and not subject_override:
            return await self.generate_smart_format_post(
                subject=planned.subject,
                smart_format="common_mistake",
                publish_to_telegram=publish_to_telegram,
                difficulty=planned.difficulty,
            )

        if planned.lane == PostLane.weekly_theme and not subject_override:
            return await self.generate_weekly_theme_post(publish_to_telegram=publish_to_telegram)

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
            # Always use text for MCQ variants so the quiz layout is preserved
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

        _FORMAT_ENUM_MAP = {
            "flashcard": ContentFormat.flashcard,
            "mnemonic": ContentFormat.mnemonic,
            "true_false": ContentFormat.true_false,
            "one_liner": ContentFormat.one_liner_recall,
            "clinical_correlation": ContentFormat.clinical_correlation,
            "comparison_table": ContentFormat.comparison_table,
            "management_algorithm": ContentFormat.management_algorithm,
            "drug_of_day": ContentFormat.drug_of_day,
            "pimp_question": ContentFormat.pimp_question,
            "spot_diagnosis": ContentFormat.spot_diagnosis,
            "ward_tip": ContentFormat.ward_tip,
            "case_unfolding": ContentFormat.case_unfolding,
            "osce_station": ContentFormat.osce_station,
            "weekly_theme_intro": ContentFormat.weekly_theme_intro,
            "common_mistake": ContentFormat.common_mistake,
            "study_schedule": ContentFormat.study_schedule,
        }

        content: GeneratedContent | None = None
        if smart_format == "flashcard":
            content = self._engine.generate_flashcard(selected_subject)
        elif smart_format == "mnemonic":
            content = self._engine.generate(selected_subject, ContentFormat.mnemonic)
        elif smart_format == "true_false":
            content = self._engine.generate_true_false(selected_subject)
        elif smart_format == "one_liner":
            content = self._engine.generate_one_liner(selected_subject)

        target_format = _FORMAT_ENUM_MAP.get(smart_format, ContentFormat.rapid_revision)

        if not content:
            content = await self.ai_client.generate(selected_subject, target_format)

        if difficulty:
            content.difficulty = difficulty.value
        self.quality_gate.validate(content)
        content = enrich_for_engagement(content)

        poster_path = Path("text-only")
        telegram_posted = False
        if publish_to_telegram:
            text = format_for_telegram(content)
            if self.settings.text_only_mode:
                telegram_posted = await self.telegram.send_message(text)
            elif self.medical_image_generator.configured:
                visual_path: Path | None = None
                try:
                    visual_path = await self.medical_image_generator.create_visual(content)
                except Exception:
                    pass
                if visual_path:
                    poster_path = visual_path
                    telegram_posted = await self.telegram.send_visual_post(visual_path, text)
                else:
                    telegram_posted = await self.telegram.send_message(text)
            else:
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
