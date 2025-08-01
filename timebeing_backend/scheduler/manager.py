from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..settings import settings

jobstores = {'default': SQLAlchemyJobStore(url=settings.DATABASE_URL)}
scheduler = AsyncIOScheduler(jobstores=jobstores)


def start_scheduler():
    if not scheduler.running:
        scheduler.start()


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
