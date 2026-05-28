"""Restart-safe scheduler with retry queue integration."""
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.config import Settings
from app.models import SlotType
from app.services.bot_commands import BotCommandHandler
from app.services.orchestrator import PostOrchestrator

logger = logging.getLogger(__name__)

_DEFAULT_SCHEDULE: list[tuple[str, SlotType]] = [
    ("08:00", SlotType.morning_revision),
    ("14:00", SlotType.afternoon_mcq),
    ("20:00", SlotType.evening_revision),
    ("22:00", SlotType.nightly_weak_topic),
]

_STATE_FILE = "logs/scheduler_state.json"


class PostingScheduler:
    def __init__(self, settings: Settings, orchestrator: PostOrchestrator) -> None:
        self.settings = settings
        self.orchestrator = orchestrator
        self.scheduler = AsyncIOScheduler(timezone=settings.timezone)
        self._cmd_handler = BotCommandHandler(
            settings=settings,
            orchestrator=orchestrator,
            telegram=orchestrator.telegram,
        )
        self._register_post_jobs()
        self._register_engagement_jobs()
        self._register_token_refresh_job()

    def start(self) -> None:
        if self.scheduler.running:
            return

        self._recover_state()
        self._register_command_polling()
        self._register_retry_job()
        self.scheduler.start()
        logger.info("Scheduler started.")

    def stop(self) -> None:
        if self.scheduler.running:
            self._save_state()
            self.scheduler.shutdown(wait=False)
            logger.info("Scheduler stopped.")

    def _register_engagement_jobs(self) -> None:
        if not self.settings.engagement_enabled:
            return

        # Daily challenge (at configured hour)
        self.scheduler.add_job(
            self._run_daily_challenge,
            trigger=CronTrigger(
                hour=self.settings.challenge_hour,
                minute=0,
                timezone=self.settings.timezone,
            ),
            id="daily_challenge",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        logger.info(
            "Daily challenge scheduled at %s:00 %s",
            self.settings.challenge_hour,
            self.settings.timezone,
        )

        # Weekly battle start (Sunday by default)
        self.scheduler.add_job(
            self._run_weekly_battle_start,
            trigger=CronTrigger(
                day_of_week=self.settings.battle_weekday,
                hour=9,
                minute=0,
                timezone=self.settings.timezone,
            ),
            id="weekly_battle_start",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        logger.info(
            "Weekly battle start scheduled on weekday %s at 09:00 %s",
            self.settings.battle_weekday,
            self.settings.timezone,
        )

        # Weekly battle end (next day)
        end_weekday = (self.settings.battle_weekday + 1) % 7
        self.scheduler.add_job(
            self._run_weekly_battle_end,
            trigger=CronTrigger(
                day_of_week=end_weekday,
                hour=8,
                minute=0,
                timezone=self.settings.timezone,
            ),
            id="weekly_battle_end",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        logger.info(
            "Weekly battle end scheduled on weekday %s at 08:00 %s",
            end_weekday,
            self.settings.timezone,
        )

    def _register_post_jobs(self) -> None:
        schedule_times = [
            t.strip()
            for t in self.settings.post_schedule_times.split(",")
            if t.strip()
        ]

        if schedule_times:
            slot_types = list(_DEFAULT_SCHEDULE)
            for i, time_str in enumerate(schedule_times):
                if i >= len(slot_types):
                    break
                _, slot_type = slot_types[i]
                try:
                    hour_str, minute_str = time_str.split(":")
                    self.scheduler.add_job(
                        self._run_job,
                        trigger=CronTrigger(
                            hour=int(hour_str),
                            minute=int(minute_str),
                            timezone=self.settings.timezone,
                        ),
                        kwargs={"slot_type": slot_type},
                        id=f"auto_post_{time_str}",
                        replace_existing=True,
                        max_instances=1,
                        coalesce=True,
                        misfire_grace_time=300,
                    )
                    logger.info(
                        "Scheduled %s at %s %s",
                        slot_type.value,
                        time_str,
                        self.settings.timezone,
                    )
                except ValueError:
                    logger.error("Invalid schedule time: %s (expected HH:MM)", time_str)
        else:
            self.scheduler.add_job(
                self._run_job,
                trigger=IntervalTrigger(hours=self.settings.post_interval_hours),
                id="auto_post_interval",
                replace_existing=True,
                max_instances=1,
                coalesce=True,
            )
            logger.info("Scheduled post every %s hour(s).", self.settings.post_interval_hours)

    def _register_command_polling(self) -> None:
        if not (self.settings.admin_chat_id and self.settings.telegram_bot_token):
            return
        self.scheduler.add_job(
            self._poll_commands,
            trigger=IntervalTrigger(seconds=30),
            id="poll_bot_commands",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        logger.info(
            "Bot command polling enabled for admin_chat_id=%s",
            self.settings.admin_chat_id,
        )

    def _register_retry_job(self) -> None:
        self.scheduler.add_job(
            self._process_retries,
            trigger=IntervalTrigger(minutes=15),
            id="retry_queue_processor",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        logger.info("Retry queue processor registered (every 15 min).")

    def _register_token_refresh_job(self) -> None:
        if not (self.settings.instagram_enabled and self.settings.facebook_app_id):
            return
        self.scheduler.add_job(
            self._refresh_instagram_token,
            trigger=IntervalTrigger(days=50),
            id="instagram_token_refresh",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        logger.info("Instagram token auto-refresh scheduled every 50 days.")

    async def _run_job(self, slot_type: SlotType | None = None) -> None:
        logger.info("Scheduled post job triggered (slot=%s).", slot_type)
        try:
            await self.orchestrator.generate_planned_post(
                publish_to_telegram=True,
                slot_type=slot_type,
            )
        except RuntimeError as exc:
            if "paused" in str(exc):
                logger.info("Skipping scheduled post — posting paused.")
                return
            logger.exception("Scheduled post failed: %s", exc)
        except Exception as exc:
            logger.exception("Scheduled post failed: %s", exc)

        # Instagram runs independently — failure never blocks Telegram
        if self.settings.instagram_enabled:
            try:
                result = await self.orchestrator.generate_instagram_post()
                if result.get("skipped"):
                    logger.info("Instagram skipped: %s", result.get("reason"))
                else:
                    logger.info(
                        "Instagram posted: %d slides, topic='%s'",
                        result.get("slide_count", 0),
                        result.get("topic", ""),
                    )
            except Exception as exc:
                logger.error("Instagram post failed (non-blocking): %s", exc)

    async def _poll_commands(self) -> None:
        try:
            await self._cmd_handler.poll()
        except Exception as exc:
            logger.debug("Command poll error: %s", exc)

    async def _process_retries(self) -> None:
        try:
            await self.orchestrator.process_retry_queue()
        except Exception as exc:
            logger.error("Retry queue processing error: %s", exc)

    async def _refresh_instagram_token(self) -> None:
        try:
            await self.orchestrator.instagram.refresh_access_token()
            logger.info("Instagram access token refreshed successfully.")
        except Exception as exc:
            logger.error("Instagram token refresh failed: %s", exc)

    # ── Engagement jobs ─────────────────────────────────────────────────────────────────────────

    async def _run_daily_challenge(self) -> None:
        logger.info("Daily challenge job triggered.")
        try:
            await self.orchestrator.generate_daily_challenge(publish_to_telegram=True)
        except Exception as exc:
            logger.exception("Daily challenge failed: %s", exc)

    async def _run_weekly_battle_start(self) -> None:
        logger.info("Weekly battle start job triggered.")
        try:
            await self.orchestrator.start_weekly_battle(publish_to_telegram=True)
        except Exception as exc:
            logger.exception("Weekly battle start failed: %s", exc)

    async def _run_weekly_battle_end(self) -> None:
        logger.info("Weekly battle end job triggered.")
        try:
            await self.orchestrator.end_weekly_battle(publish_to_telegram=True)
        except Exception as exc:
            logger.exception("Weekly battle end failed: %s", exc)

    # ── Restart safety ────────────────────────────────────────────────────────────────────────────

    def _save_state(self) -> None:
        try:
            path = Path(_STATE_FILE)
            path.parent.mkdir(parents=True, exist_ok=True)
            state = {
                "saved_at": datetime.now(tz=timezone.utc).isoformat(),
                "cursor": getattr(self.orchestrator.content_strategy, "_cursor", 0),
                "paused": self.orchestrator.paused,
            }
            path.write_text(json.dumps(state, indent=2), encoding="utf-8")
            logger.debug("Scheduler state saved.")
        except Exception as exc:
            logger.warning("Could not save scheduler state: %s", exc)

    def _recover_state(self) -> None:
        path = Path(_STATE_FILE)
        if not path.exists():
            return
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
            paused = state.get("paused", False)
            if paused:
                self.orchestrator.pause()
                logger.info("Recovered paused state from last shutdown.")
            else:
                logger.info("Scheduler recovered: posting was active.")
            path.unlink(missing_ok=True)
        except Exception as exc:
            logger.warning("Could not recover scheduler state: %s", exc)
