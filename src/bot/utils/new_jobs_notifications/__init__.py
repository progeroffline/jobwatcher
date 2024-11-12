import asyncio
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from bot.repositories.job_vacancy import JobVacancyRepository
from bot.repositories.user import UserRepository
from . import artstation, belmeta, jobsua, olx, rabotaua, workaua
from .notifications_queue import notifications_queue


class NewJobsNotifications:
    def __init__(self, sessionmaker: async_sessionmaker):
        self.sessionmaker = sessionmaker
        self.scheduler = AsyncIOScheduler()
        self.user_repository = UserRepository(sessionmaker())

    async def send_notification(
        self,
        bot: Bot,
        user_id: int,
        vacancy: dict[str, str | int],
    ) -> None:
        await bot.send_message(chat_id=user_id, text=str(vacancy["title"]))
        await asyncio.sleep(0.1)

    async def send_notifications_for_job(self, bot: Bot) -> None:
        while True:
            vacancy = await notifications_queue.get()

            async for user_id in self.user_repository.get_all():
                await self.send_notification(bot, user_id, vacancy)

            notifications_queue.task_done()

    async def scrap_data(self) -> None:
        async with self.sessionmaker() as session:
            await artstation.scrap_data(JobVacancyRepository(session))
            await belmeta.scrap_data(JobVacancyRepository(session))
            await jobsua.scrap_data(JobVacancyRepository(session))
            await olx.scrap_data(JobVacancyRepository(session))
            await rabotaua.scrap_data(JobVacancyRepository(session))
            await workaua.scrap_data(JobVacancyRepository(session))

    async def start(self, bot: Bot) -> None:
        self.scheduler.add_job(
            self.scrap_data,
            trigger=IntervalTrigger(minutes=5),
            max_instances=1,
        )
        self.scheduler.start()
        asyncio.create_task(self.send_notifications_for_job(bot))
