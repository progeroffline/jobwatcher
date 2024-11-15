from typing import Optional, Sequence, AsyncGenerator

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from bot.database.models.job_vacancy_categories import JobVacancyCategory
from bot.database.models.user import User
from bot.repositories.abstracts import BaseRepository


class UserRepository(BaseRepository):
    async def create(
        self,
        id: int,
        name: Optional[str] = None,
        username: Optional[str] = None,
    ) -> User:
        user = User(id=id, name=name, username=username)
        self._session.add(user)
        await self._session.commit()
        return user

    async def get_subscriptions(self, user_id: int) -> Sequence[JobVacancyCategory]:
        user = await self.get_user_by_id(user_id)
        if user is None:
            return []
        return user.subscribed_categories

    async def enable_subscription_to_category(
        self,
        user_id: int,
        category: Optional[JobVacancyCategory] = None,
        categories: Sequence[JobVacancyCategory] = [],
    ) -> None:
        user = await self.get_user_by_id(user_id)
        if user is None:
            return

        if category is not None:
            user.subscribed_categories.append(category)
        else:
            for category in categories:
                if category not in user.subscribed_categories:
                    user.subscribed_categories.append(category)
        await self._session.commit()

    async def disable_subscription_to_category(
        self,
        user_id: int,
        category: Optional[JobVacancyCategory] = None,
    ) -> None:
        user = await self.get_user_by_id(user_id)
        if user is None:
            return

        if category is None:
            user.subscribed_categories.clear()
        else:
            user.subscribed_categories.remove(category)

        await self._session.commit()

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = (
            select(User)
            .options(selectinload(User.subscribed_categories))
            .where(User.id == user_id)
        )
        return await self._session.scalar(query)

    async def exists(
        self,
        id: Optional[int] = None,
        username: Optional[str] = None,
    ) -> bool:
        query = None

        if id:
            query = select(User.id).filter_by(id=id).limit(1)
        if username:
            query = select(User.id).filter_by(username=username).limit(1)

        if query is not None:
            return await self._session.scalar(query) is not None
        return False

    async def is_admin(self, id: int) -> bool:
        query = select(User.is_admin).where(User.id == id)
        result = await self._session.scalar(query)
        return bool(result)

    async def set_admin_by_username(self, username: str) -> None:
        query = (
            update(User)
            .where(User.username == username)
            .values(is_admin=True)
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(query)
        await self._session.commit()

    async def unset_admin_by_username(self, username: str) -> None:
        query = (
            update(User)
            .where(User.username == username)
            .values(is_admin=False)
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(query)
        await self._session.commit()

    async def get_admins(self) -> Sequence[User]:
        query = select(User).where(User.is_admin)
        result = await self._session.scalars(query)
        return result.all()

    async def get_all(self) -> AsyncGenerator[int, None]:
        result = await self._session.stream(select(User.id))

        async for row in result:
            yield row.id
