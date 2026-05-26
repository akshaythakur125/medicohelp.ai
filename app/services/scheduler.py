import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.config import Settings
from app.models import SlotType
from app.services.bot_commands import BotCommandHandler
from app.services.orchestrator import PostOrchestrator

logger = logging.getLogger(__name__)

# Four-phase day schedule (IST)
_DEFAULT_SCHEDULE: list[tuple[str, SlotType]] = [
    ("08:00", SlotType.morning_revision),
    ("14:00", SlotType.afternoon_mcq),
    ("20:00", SlotType.evening_revision),
    ("22:00", SlotType.nightly_weak_topic),
]


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

        self._register_command_polling()
        self.scheduler.start()
        logger.info("Scheduler started.")

    def stop(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            logger.info("Scheduler stopped.")

    def _register_post_jobs(self) -> None:
        schedule_times = [
            t.strip()
            for t in self.settings.post_schedule_times.split(",")
            if t.strip()
        ]

        if schedule_times:
            # Use configured HH:MM slots — map by index to SlotType
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
            # Fallback: interval-based posting
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

    async def _run_job(self, slot_type: SlotType | None = None) -> None:
        logger.info("Scheduled post job triggered (slot=%s).", slot_type)
        try:
            await self.orchestrator.generate_planned_post(
                publish_to_telegram=True,
                slot_type=slot_type,
            )
        except Exception as exc:
            logger.exception("Scheduled post failed: %s", exc)

    async def _poll_commands(self) -> None:
        try:
            await self._cmd_handler.poll()
        except Exception as exc:
            logger.debug("Command poll error: %s", exc)
