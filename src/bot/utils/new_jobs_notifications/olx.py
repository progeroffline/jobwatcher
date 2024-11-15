from bot.repositories.job_vacancy import JobVacancyRepository
from bot.services.olx import OlxParser
from .notifications_queue import notifications_queue


async def scrap_data(job_vacancy_repository: JobVacancyRepository):
    service = OlxParser()
    response = await service.search()

    for job_vacancy in response:
        service_id = await job_vacancy_repository.get_service_id(
            service_name="olx",
            service_id=job_vacancy["category"]["service_id"],  # type: ignore
        )
        category = await job_vacancy_repository.get_category(id=service_id.category_id)
        job_vacancy["category"]["name"] = category.name  # type: ignore

        if not await job_vacancy_repository.exists(str(job_vacancy["id"])):
            await job_vacancy_repository.create(**job_vacancy)  # type: ignore
            await notifications_queue.put(job_vacancy)
