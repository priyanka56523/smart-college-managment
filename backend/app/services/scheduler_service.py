"""Background Task Scheduler using APScheduler for periodic ingestion and briefing runs."""
import logging
import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.config import settings
from app.database import SessionLocal
from app.services.ingestion_pipeline import run_ingestion_pipeline
from app.services.reporting_service import ReportingService

logger = logging.getLogger(__name__)

class PlatformScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False

    def start(self):
        """Start the background scheduler with configured intervals."""
        if not settings.SCHEDULER_ENABLED:
            logger.info("Background scheduler is disabled by configuration.")
            return

        # Periodic ingestion job (default every 6 hours)
        self.scheduler.add_job(
            self._scheduled_ingestion_job,
            trigger=IntervalTrigger(hours=settings.SCHEDULER_INTERVAL_HOURS),
            id="periodic_ingestion",
            name="Periodic Ingestion & Verification",
            replace_existing=True,
            next_run_time=None  # Can be triggered manually or waits for next cycle
        )

        # Daily executive intelligence briefing job (every 24 hours)
        self.scheduler.add_job(
            self._scheduled_report_job,
            trigger=IntervalTrigger(hours=24),
            id="daily_intelligence_briefing",
            name="Daily Executive Briefing Generator",
            replace_existing=True
        )

        self.scheduler.start()
        self.is_running = True
        logger.info(f"Platform scheduler started. Ingestion interval: {settings.SCHEDULER_INTERVAL_HOURS} hours.")

    def shutdown(self):
        """Gracefully stop background scheduler."""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Platform scheduler shut down.")

    async def _scheduled_ingestion_job(self):
        """Asynchronous execution worker for scheduled ingestion."""
        logger.info(f"Executing scheduled ingestion cycle at {datetime.utcnow().isoformat()}...")
        db = SessionLocal()
        try:
            result = await run_ingestion_pipeline(db)
            logger.info(f"Scheduled ingestion completed: {result}")
        except Exception as e:
            logger.error(f"Scheduled ingestion error: {e}")
        finally:
            db.close()

    async def _scheduled_report_job(self):
        """Generate daily intelligence report."""
        logger.info("Generating scheduled daily intelligence briefing...")
        db = SessionLocal()
        try:
            report = ReportingService.generate_briefing(db, report_type="daily", period_hours=24)
            logger.info(f"Generated daily report: ID {report.id} - '{report.title}'")
        except Exception as e:
            logger.error(f"Scheduled briefing error: {e}")
        finally:
            db.close()

platform_scheduler = PlatformScheduler()
