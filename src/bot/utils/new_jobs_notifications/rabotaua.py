from bot.repositories.job_vacancy import JobVacancyRepository
from bot.services.rabotaua import RabotaUAParser
from .notifications_queue import notifications_queue


async def scrap_data(job_vacancy_respository: JobVacancyRepository):
    service = RabotaUAParser()
    response = await service.search()

    for job_vacancy in response:
        service_id = await job_vacancy_respository.get_service_id(
            service_name="rabotaua",
            service_id=job_vacancy["category"]["service_id"],  # type: ignore
        )
        category = await job_vacancy_respository.get_category(id=service_id.category_id)
        job_vacancy["category"]["name"] = category.name  # type: ignore

        if not await job_vacancy_respository.exists(str(job_vacancy["id"])):
            await job_vacancy_respository.create(**job_vacancy)  # type: ignore
            await notifications_queue.put(job_vacancy)
