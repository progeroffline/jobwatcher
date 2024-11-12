import asyncio
from abc import ABC
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    def __init__(self, session: AsyncSession):
        self._session = session

    def __del__(self):
        asyncio.create_task(self._session.close())
