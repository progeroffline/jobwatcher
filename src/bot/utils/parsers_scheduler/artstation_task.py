from bot.repositories.job_vacancy import JobVacancyRepository
from bot.services.artstation import ArtStationParser


async def task(job_vacancy_respository: JobVacancyRepository):
    service = ArtStationParser()
    response = await service.search()

    for job_vacancy in response:
        await job_vacancy_respository.create(**job_vacancy)
