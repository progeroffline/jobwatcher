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
from bot.dependencies import settings, logger
from . import artstation, belmeta, jobsua, olx, rabotaua, workaua
from .notifications_queue import notifications_queue


class NewJobsNotifications:
    def __init__(self, sessionmaker: async_sessionmaker):
        logger.debug("Init NewJobsNotifications service")
        self.sessionmaker = sessionmaker
        self.scheduler = AsyncIOScheduler()
        self.first_launch = True

    async def send_notification(
        self,
        bot: Bot,
        user_id: int,
        vacancy: dict[str, str | int],
    ) -> None:
        await bot.send_message(chat_id=user_id, text=str(vacancy["title"]))
        await asyncio.sleep(0.1)
        logger.debug(f"Successfully sent notification for user ID: {user_id}")

    async def send_notifications_for_job(self, bot: Bot) -> None:
        logger.debug("Send notifications about new job to users")
        async with self.sessionmaker() as session:
            user_repository = UserRepository(session)
            while True:
                vacancy = await notifications_queue.get()
                logger.debug(f"Got new vacancy from queue {vacancy['id']}")
                logger.debug(f"Remove vacancy from queue {vacancy['id']}")
                notifications_queue.task_done()

                if self.first_launch:
                    logger.debug("Skip sending notification cause it is a first launch")
                    continue

                async for user_id in user_repository.get_all():
                    try:
                        if settings.noitify_users_about_new_vacancies:
                            await self.send_notification(bot, user_id, vacancy)
                        else:
                            logger.debug(
                                "Skip sending notification cause notifications disabled by admin"
                            )
                    except TelegramForbiddenError:
                        logger.debug(
                            f"Skip sending notification cause bot blocked by user ID: {user_id}"
                        )
                    except Exception as error:
                        logger.error(
                            f"Got error when trying sent notification to user ser ID: {user_id},"
                            f"Error: {error}"
                        )

    async def make_post_to_channel(self, bot: Bot) -> None:
        logger.debug("Send notifications about new job to channels")
        async with self.sessionmaker() as session:
            job_vacancy_repository = JobVacancyRepository(session)
            channel_repository = ChannelRepository(session)
            channels = await channel_repository.get_all()
            vacancies = await job_vacancy_repository.get_not_sent_to_channel()
            now = datetime.now()

            for channel in channels:
                logger.debug(
                    f"Check channel ID: {channel.id}, "
                    f"Title: {channel.title}, "
                    f"Post interval: {channel.post_interval}"
                )
                if now.minute % channel.post_interval != 0:
                    logger.debug(
                        f"Skip channel ID: {channel.id}, "
                        f"Title: {channel.title}, "
                        f"Post interval: {channel.post_interval}"
                    )

                    continue
                for vacancy in vacancies:
                    logger.debug(
                        f"Send vacancies to channel ID: {channel.id}, "
                        f"Title: {channel.title}, "
                        f"Post interval: {channel.post_interval}"
                    )
                    await self.send_notification(bot, channel.id, vacancy.to_dict())
                    await job_vacancy_repository.mark_as_sent_to_channel(vacancy.id)
                    await asyncio.sleep(3)

    async def scrap_data(self) -> None:
        logger.debug("Scrap vacancies from sites")
        async with self.sessionmaker() as session:
            logger.debug("Scrap vacancies from artstation site")
            await artstation.scrap_data(JobVacancyRepository(session))

            logger.debug("Scrap vacancies from belmeta site")
            await belmeta.scrap_data(JobVacancyRepository(session))

            logger.debug("Scrap vacancies from jobsua site")
            await jobsua.scrap_data(JobVacancyRepository(session))

            logger.debug("Scrap vacancies from olx site")
            await olx.scrap_data(JobVacancyRepository(session))

            logger.debug("Scrap vacancies from rabotaua site")
            await rabotaua.scrap_data(JobVacancyRepository(session))

            logger.debug("Scrap vacancies from workaua site")
            await workaua.scrap_data(JobVacancyRepository(session))
            self.first_launch = False

    async def start(self, bot: Bot) -> None:
        logger.debug("Create tasks for NewJobsNotifications service")
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
        logger.debug("Start scheduler for NewJobsNotifications service")
        self.scheduler.start()

        logger.debug("Bind send_notifications_for_job for NewJobsNotifications service")
        asyncio.create_task(self.send_notifications_for_job(bot))
