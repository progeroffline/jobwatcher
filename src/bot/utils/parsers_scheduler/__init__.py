from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bot.repositories.job_vacancy import JobVacancyRepository
from . import (
    artstation_task,
    belmeta_task,
    jobsua_task,
    olx_task,
    rabotaua_task,
    workaua_task,
)


async def scrap_data_task(job_vacancy_repository: JobVacancyRepository) -> None:
    await artstation_task.scrap_data(job_vacancy_repository)
    await belmeta_task.scrap_data(job_vacancy_repository)
    await jobsua_task.scrap_data(job_vacancy_repository)
    await olx_task.scrap_data(job_vacancy_repository)
    await rabotaua_task.scrap_data(job_vacancy_repository)
    await workaua_task.scrap_data(job_vacancy_repository)


def create_parser_scheduler(
    job_vacancy_repository: JobVacancyRepository,
) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        scrap_data_task,
        trigger=IntervalTrigger(seconds=10),
        max_instances=1,
        args=(job_vacancy_repository,),
    )

    return scheduler
