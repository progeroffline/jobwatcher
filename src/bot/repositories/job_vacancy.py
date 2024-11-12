from typing import Sequence
from sqlalchemy import select, update
from bot.database.models import JobVacancy
from bot.database.models.job_vacancy import JobVacancyLocation
from bot.repositories.abstracts import BaseRepository


class JobVacancyRepository(BaseRepository):
    async def create_location(self, **kwargs) -> JobVacancyLocation:
        job_vacancy_location = JobVacancyLocation(**kwargs)
        self._session.add(job_vacancy_location)
        await self._session.commit()
        return job_vacancy_location

    async def get_location(self, **kwargs) -> JobVacancyLocation:
        stmt = select(JobVacancyLocation).filter_by(**kwargs)
        result = (await self._session.execute(stmt)).scalar_one_or_none()
        if result is None:
            return await self.create_location(**kwargs)
        return result

    async def create(
        self,
        id: str,
        locations: list[dict[str, str]],
        **kwargs,
    ) -> JobVacancy:
        locations = [await self.get_location(**location) for location in locations]
        job_vacancy = await self.get(id=id)
        if job_vacancy is not None:
            return job_vacancy  # Return value if it exists in db

        job_vacancy = JobVacancy(id=id, locations=locations, **kwargs)
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

    async def get_not_sent_to_channel(self) -> Sequence[JobVacancy]:
        stmt = select(JobVacancy).where(JobVacancy.sent_to_channel.is_(False))
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def mark_as_sent_to_channel(self, id: str) -> JobVacancy:
        stmt = (
            update(JobVacancy).values(sent_to_channel=True).where(JobVacancy.id == id)
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return await self.get(id)
