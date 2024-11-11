from bot.database.models import JobVacancy
from bot.repositories.abstracts import BaseRepository


class JobVacancyRepository(BaseRepository):
    async def create(self, **kwargs) -> JobVacancy:
        print("Create by kwars", kwargs)
        job_vacancy = JobVacancy(**kwargs)
        self._session.add(job_vacancy)
        await self._session.commit()
        return job_vacancy
