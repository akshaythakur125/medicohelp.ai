import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.config import Settings
from app.services.bot_commands import BotCommandHandler
from app.services.orchestrator import PostOrchestrator

logger = logging.getLogger(__name__)


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

    def start(self) -> None:
        if self.scheduler.running:
            return

        self._register_post_jobs()
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
            for time_str in schedule_times:
                try:
                    hour_str, minute_str = time_str.split(":")
                    self.scheduler.add_job(
                        self._run_job,
                        trigger=CronTrigger(
                            hour=int(hour_str),
                            minute=int(minute_str),
                            timezone=self.settings.timezone,
                        ),
                        id=f"auto_post_{time_str}",
                        replace_existing=True,
                        max_instances=1,
                        coalesce=True,
                    )
                    logger.info("Scheduled post at %s %s", time_str, self.settings.timezone)
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
        logger.info("Bot command polling enabled for admin_chat_id=%s", self.settings.admin_chat_id)

    async def _run_job(self) -> None:
        logger.info("Scheduled post job triggered.")
        try:
            await self.orchestrator.generate_planned_post(publish_to_telegram=True)
        except Exception as exc:
            logger.exception("Scheduled post failed: %s", exc)

    async def _poll_commands(self) -> None:
        try:
            await self._cmd_handler.poll()
        except Exception as exc:
            logger.debug("Command poll error: %s", exc)
