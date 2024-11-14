from typing import Sequence
from sqlalchemy import select, update
from bot.database.models.job_vacancy import JobVacancy
from bot.database.models.job_vacancy_location import JobVacancyLocation
from bot.database.models.job_vacancy_categories import JobVacancyCategory
from bot.database.models.job_vacancy_service_id import JobVacancyCategoryServiceID
from bot.repositories.abstracts import BaseRepository


class JobVacancyRepository(BaseRepository):
    async def create_service_id(self, **kwargs) -> JobVacancyCategoryServiceID:
        job_vacancy_category = JobVacancyCategoryServiceID(**kwargs)
        self._session.add(job_vacancy_category)
        await self._session.commit()
        return job_vacancy_category

    async def get_service_id(self, **kwargs) -> JobVacancyCategoryServiceID:
        stmt = select(JobVacancyCategoryServiceID).filter_by(**kwargs)
        result = (await self._session.execute(stmt)).scalar_one_or_none()
        if result is None:
            return await self.create_service_id(**kwargs)
        return result

    async def create_category(self, **kwargs) -> JobVacancyCategory:
        job_vacancy_category = JobVacancyCategory(**kwargs)
        self._session.add(job_vacancy_category)
        await self._session.commit()
        return job_vacancy_category

    async def get_category(self, **kwargs) -> JobVacancyCategory:
        stmt = select(JobVacancyCategory).filter_by(**kwargs)
        result = (await self._session.execute(stmt)).scalar_one_or_none()
        if result is None:
            return await self.create_category(**kwargs)
        return result

    async def get_categories(self) -> Sequence[JobVacancyCategory]:
        stmt = select(JobVacancyCategory)
        result = await self._session.execute(stmt)
        return result.scalars().all()

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
        category: dict[str, str | int],
        **kwargs,
    ) -> JobVacancy:
        locations = [await self.get_location(**location) for location in locations]
        db_category = await self.get_category(name=category["name"])  # type: ignore
        await self.get_service_id(
            service_name=category["service_name"],
            service_id=category["service_id"],
            category_id=db_category.id,
        )

        job_vacancy = await self.get(id=id)
        if job_vacancy is not None:
            return job_vacancy  # Return value if it exists in db

        job_vacancy = JobVacancy(
            id=id,
            locations=locations,
            category_id=db_category.id,
            **kwargs,
        )
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
