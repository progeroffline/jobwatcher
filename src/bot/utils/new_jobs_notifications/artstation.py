from bot.repositories.job_vacancy import JobVacancyRepository
from bot.services.artstation import ArtStationParser
from .notifications_queue import notifications_queue


async def scrap_data(job_vacancy_repository: JobVacancyRepository):
    service = ArtStationParser()

    for category in await job_vacancy_repository.get_categories():
        vacancies = await service.search(query_en=category.name_en)
        for job_vacancy in vacancies:
            if not await job_vacancy_repository.exists(str(job_vacancy["id"])):
                job_vacancy["category_id"] = category.id

                await job_vacancy_repository.create(**job_vacancy)  # type: ignore

                job_vacancy["category_name"] = category.name

                await notifications_queue.put(job_vacancy)
