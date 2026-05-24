import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.config import Settings
from app.services.orchestrator import PostOrchestrator

logger = logging.getLogger(__name__)


class PostingScheduler:
    def __init__(self, settings: Settings, orchestrator: PostOrchestrator) -> None:
        self.settings = settings
        self.orchestrator = orchestrator
        self.scheduler = AsyncIOScheduler(timezone=settings.timezone)

    def start(self) -> None:
        if self.scheduler.running:
            return

        self.scheduler.add_job(
            self._run_job,
            trigger=IntervalTrigger(hours=self.settings.post_interval_hours),
            id="auto_generate_and_post",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        self.scheduler.start()
        logger.info("Scheduler started. Interval: %s hours", self.settings.post_interval_hours)

    def stop(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            logger.info("Scheduler stopped.")

    async def _run_job(self) -> None:
        logger.info("Scheduled post job started.")
        await self.orchestrator.generate_planned_post(publish_to_telegram=True)
