import asyncio
from datetime import datetime
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from bot.repositories.channel import ChannelRepository
from bot.repositories.job_vacancy import JobVacancyRepository
from bot.repositories.user import UserRepository
from bot.dependencies import settings
from . import artstation, belmeta, jobsua, olx, rabotaua, workaua
from .notifications_queue import notifications_queue


class NewJobsNotifications:
    def __init__(self, sessionmaker: async_sessionmaker):
        self.sessionmaker = sessionmaker
        self.scheduler = AsyncIOScheduler()
        self.first_launch = True

    async def send_notification(
        self,
        bot: Bot,
        user_id: int,
        vacancy: dict[str, str | int],
    ) -> None:
        if settings.noitify_users_about_new_vacancies:
            await bot.send_message(chat_id=user_id, text=str(vacancy["title"]))
        await asyncio.sleep(0.1)

    async def send_notifications_for_job(self, bot: Bot) -> None:
        async with self.sessionmaker() as session:
            user_repository = UserRepository(session)
            while True:
                vacancy = await notifications_queue.get()
                notifications_queue.task_done()

                if self.first_launch:
                    continue

                async for user_id in user_repository.get_all():
                    try:
                        await self.send_notification(bot, user_id, vacancy)
                    except TelegramForbiddenError:
                        pass
                    except Exception as e:
                        print(e)

    async def make_post_to_channel(self, bot: Bot) -> None:
        async with self.sessionmaker() as session:
            job_vacancy_repository = JobVacancyRepository(session)
            channel_repository = ChannelRepository(session)
            channels = await channel_repository.get_all()
            vacancies = await job_vacancy_repository.get_not_sent_to_channel()
            now = datetime.now()

            for channel in channels:
                if now.minute % channel.post_interval != 0:
                    continue
                for vacancy in vacancies:
                    await self.send_notification(bot, channel.id, vacancy.to_dict())
                    await job_vacancy_repository.mark_as_sent_to_channel(vacancy.id)
                    await asyncio.sleep(3)

    async def scrap_data(self) -> None:
        async with self.sessionmaker() as session:
            await artstation.scrap_data(JobVacancyRepository(session))
            await belmeta.scrap_data(JobVacancyRepository(session))
            await jobsua.scrap_data(JobVacancyRepository(session))
            await olx.scrap_data(JobVacancyRepository(session))
            await rabotaua.scrap_data(JobVacancyRepository(session))
            await workaua.scrap_data(JobVacancyRepository(session))
            self.first_launch = False

    async def start(self, bot: Bot) -> None:
        self.scheduler.add_job(
            self.scrap_data,
            trigger=IntervalTrigger(minutes=1),
            max_instances=1,
        )
        self.scheduler.add_job(
            self.make_post_to_channel,
            "interval",
            minutes=2,
            args=(bot,),
        )
        self.scheduler.start()
        asyncio.create_task(self.send_notifications_for_job(bot))
