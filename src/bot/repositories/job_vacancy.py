from sqlalchemy import select
from bot.database.models import JobVacancy
from bot.repositories.abstracts import BaseRepository


class JobVacancyRepository(BaseRepository):
    async def create(self, **kwargs) -> JobVacancy:
        job_vacancy = await self.get(id=kwargs["id"])
        if job_vacancy is not None:
            return job_vacancy  # Return value if it exists in db

        job_vacancy = JobVacancy(**kwargs)
        self._session.add(job_vacancy)
        await self._session.commit()
        return job_vacancy

    async def get(self, id: str) -> JobVacancy | None:
        stmt = select(JobVacancy).where(JobVacancy.id == id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists(self, id: str) -> bool:
        query = select(JobVacancy.id).filter_by(id=id).limit(1)
        return await self._session.scalar(query) is not None
