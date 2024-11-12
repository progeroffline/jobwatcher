from bot.repositories.job_vacancy import JobVacancyRepository
from bot.services.workua import WorkUAParser
from .notifications_queue import notifications_queue


async def scrap_data(job_vacancy_respository: JobVacancyRepository):
    service = WorkUAParser()
    response = await service.search()

    for job_vacancy in response:
        if not await job_vacancy_respository.exists(str(job_vacancy["id"])):
            await job_vacancy_respository.create(**job_vacancy)  # type: ignore
            await notifications_queue.put(job_vacancy)
