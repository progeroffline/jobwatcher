from bot.repositories.job_vacancy import JobVacancyRepository
from bot.services.workua import WorkUAParser


async def scrap_data(job_vacancy_respository: JobVacancyRepository):
    service = WorkUAParser()
    response = await service.search()

    for job_vacancy in response:
        await job_vacancy_respository.create(**job_vacancy)  # type: #ignore
