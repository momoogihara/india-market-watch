from apscheduler.schedulers.background import BackgroundScheduler
from app.core.logger import get_logger

logger = get_logger()

scheduler = BackgroundScheduler()

def job():
    logger.info("scheduled job running")

def start_scheduler():
     if not scheduler.running:
        scheduler.add_job(job, "interval", minutes=10, id="job1", replace_existing=True)
        scheduler.start()
        logger.info("scheduler started")