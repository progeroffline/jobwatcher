from sqlalchemy import select

from bot.database.models import Channel
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
