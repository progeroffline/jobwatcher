from bot.repositories.job_vacancy import JobVacancyRepository
from bot.services.jobsua import JobsUAParser


async def scrap_data(job_vacancy_respository: JobVacancyRepository):
    service = JobsUAParser()
    response = await service.search()

    for job_vacancy in response:
        await job_vacancy_respository.create(**job_vacancy)  # type: ignore
