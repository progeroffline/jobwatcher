from rich import print
from bot.services.{service_package} import {service_class}
from bot.repositories.job_vacancy import JobVacancyRepository
from bot.dependencies import sessionmaker


async def test():
    async with sessionmaker() as session:
        job_vacancy_repository = JobVacancyRepository(session)

        for i in range(10):
            service = {service_class}()

            response = await service.search(page=i + 1)
            for job_vacancy in response:
                print(job_vacancy)
                await job_vacancy_repository.create(**job_vacancy)  # type: ignore
