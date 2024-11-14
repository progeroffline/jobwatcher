from typing import Sequence
from sqlalchemy import delete, select, update

from bot.database.models.channel import Channel
from bot.repositories.abstracts import BaseRepository


class ChannelRepository(BaseRepository):
    async def create(self, **kwargs) -> Channel:
        user = Channel(**kwargs)
        self._session.add(user)
        await self._session.commit()
        return user

    async def get(self, id: int) -> Channel:
        stmt = select(Channel).where(Channel.id == id)
        result = await self._session.execute(stmt)
        return result.scalar()

    async def get_all(self) -> Sequence[Channel]:
        stmt = select(Channel)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def delete(self, id: int) -> None:
        stmt = delete(Channel).where(Channel.id == id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def exists(self, id: str) -> bool:
        stmt = select(Channel.id).filter_by(id=id).limit(1)
        return await self._session.scalar(stmt) is not None

    async def update(self, id: int, **kwargs) -> Channel:
        stmt = update(Channel).values(**kwargs).where(Channel.id == id)
        await self._session.execute(stmt)
        await self._session.commit()
        return await self.get(id)
