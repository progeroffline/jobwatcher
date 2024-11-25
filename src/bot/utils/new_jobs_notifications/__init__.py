import asyncio
from datetime import datetime
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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
        self.service_objects = {
            "artstation": artstation,
            "belmeta": belmeta,
            "jobsua": jobsua,
            "olx": olx,
            "rabotaua": rabotaua,
            "workua": workaua,
        }
        self.service_launched = {
            "artstation": False,
            "belmeta": False,
            "jobsua": True,
            "olx": False,
            "rabotaua": False,
            "workua": False,
        }

    @staticmethod
    def user_subscribed_to_vacancy(
        vacancy_category: list[str],
        vacancy_keywords: list[str],
        vacancy_region: list[str],
        categories: list[str],
        keywords: list[str],
        regions: list[str],
    ) -> bool:
        if not vacancy_category or not vacancy_region:
            return False

        vacancy_category_set = set(vacancy_category)
        vacancy_keywords_set = set([item.lower() for item in vacancy_keywords if item])
        vacancy_region_set = set(vacancy_region)

        selected_categories = set(categories)
        selected_keywords = set([item.lower() for item in keywords if item])
        selected_regions = set(regions)

        matches_category = (
            not selected_categories
        ) or vacancy_category_set.intersection(selected_categories)
        matches_keywords = not selected_keywords or vacancy_keywords_set.intersection(
            selected_keywords
        )
        matches_region = not selected_regions or vacancy_region_set.intersection(
            selected_regions
        )
        return bool(matches_category and matches_keywords and matches_region)

    async def send_notification(
        self,
        bot: Bot,
        user_id: int,
        vacancy: dict[str, str | int | list[dict[str, str]]],
    ) -> None:
        salary = f"{vacancy['min_salary']} - {vacancy['max_salary']}"
        salary = (
            "Не указано"
            if salary == "0 - 0"
            else f"{salary} {vacancy['salary_currency']}"
        )
        message = "".join(
            [
                f"<b>✨ {vacancy['title']}</b>\n\n",
                f"<b>🏢 Компания:</b> {vacancy['company']}\n",
                f"<b>💰 Зарплата</b>: {salary}\n",
                f"<b>📅 Период:</b> {vacancy['salary_period']}\n",
                f"<b>📍 Категория:</b> {vacancy['category_name']}\n",  # type: ignore
                f"<b>🌐 Локация:</b> {','.join([location['city'] for location in vacancy['locations']])}\n\n",  # type: ignore
                f"<b>📄 Описание:</b> {str(vacancy['description'])[:settings.vacancy_description_max_preview_chars]}...\n",
            ]
        )
        try:
            await bot.send_message(
                chat_id=user_id,
                text=message,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="👀 Перейти к вакансии",
                                url=str(vacancy["url"]),
                            ),
                        ]
                    ]
                ),
            )
            await asyncio.sleep(0.1)
            logger.debug(f"Successfully sent notification for user ID: {user_id}")
        except TelegramForbiddenError:
            logger.debug(
                f"Skip sending notification cause bot blocked by user ID: {user_id}"
            )
        except Exception as error:
            logger.error(
                f"Got error when trying sent notification to user ser ID: {user_id},"
                f"Error: {error}"
            )

    async def send_notifications_for_job(self, bot: Bot) -> None:
        logger.debug("Send notifications about new job to users")
        async with self.sessionmaker() as session:
            user_repository = UserRepository(session)
            job_vacancy_repository = JobVacancyRepository(session)
            while True:
                vacancy = await notifications_queue.get()
                logger.debug(f"Got new vacancy from queue {vacancy['id']}")
                logger.debug(f"Remove vacancy from queue {vacancy['id']}")
                notifications_queue.task_done()

                if not settings.noitify_users_about_new_vacancies:
                    continue

                category = await job_vacancy_repository.get_category(
                    id=vacancy["category_id"],
                )
                logger.debug(f"Get vacancy category by id {category.id}")

                # if not all(self.service_launched.values()):
                #     logger.debug(
                #         f"Skip sending notification cause not all services lauched {self.service_launched}"
                #     )
                #     continue

                async for user in user_repository.get_all(category_id=category.id):
                    if self.user_subscribed_to_vacancy(
                        vacancy_category=[category.name],
                        vacancy_keywords=vacancy["title"].split(),
                        vacancy_region=[
                            location["country"] for location in vacancy["locations"]
                        ],
                        categories=[
                            category.name for category in user.subscribed_categories
                        ],
                        keywords=(
                            keywords.split(",")
                            if (keywords := user.subscribed_keyword) is not None
                            else []
                        ),
                        regions=[region.region for region in user.subscribed_regions],
                    ):
                        await self.send_notification(bot, user.id, vacancy)

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

    async def scrap_data(self, service_name: str) -> None:
        async with self.sessionmaker() as session:
            logger.debug(f"Scrap vacancies from {service_name} site")
            await self.service_objects[service_name].scrap_data(
                JobVacancyRepository(session)
            )

            self.service_launched[service_name] = True

    async def start(self, bot: Bot) -> None:
        logger.debug("Create tasks for NewJobsNotifications service")

        for service_name in self.service_objects.keys():
            self.scheduler.add_job(
                self.scrap_data,
                trigger=IntervalTrigger(minutes=1),
                max_instances=10,
                args=(service_name,),
            )
        self.scheduler.add_job(
            self.make_post_to_channel,
            "interval",
            minutes=1,
            args=(bot,),
        )
        logger.debug("Start scheduler for NewJobsNotifications service")
        self.scheduler.start()

        logger.debug("Bind send_notifications_for_job for NewJobsNotifications service")
        asyncio.create_task(self.send_notifications_for_job(bot))
