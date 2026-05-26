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

    # ── Restart safety ───────────────────────────────────────────────────

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
