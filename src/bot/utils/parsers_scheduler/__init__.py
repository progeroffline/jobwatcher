from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.repositories.job_vacancy import JobVacancyRepository
from . import artstation_task


def create_parser_scheduler(
    job_vacancy_repository: JobVacancyRepository,
) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        artstation_task.task,
        "interval",
        seconds=10,
        args=(job_vacancy_repository,),
    )
    return scheduler
