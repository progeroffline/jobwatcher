from pathlib import Path
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore
from bot.config_reader import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.middlewares.session_provider import SessionProviderMiddleware
from bot.middlewares.repository_provider import RepositoryProviderMiddleware
from bot.repositories.channel import ChannelRepository
from bot.repositories.job_vacancy import JobVacancyRepository
from bot.repositories.user import UserRepository
from bot.utils.custom_logger import create_logger
from bot.utils.new_jobs_notifications import NewJobsNotifications

logger = create_logger(settings.logger_logfile_path)
engine = create_async_engine(url=settings.get_postgres_dsn_url(), echo=False)
sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

session_provider = SessionProviderMiddleware(sessionmaker=sessionmaker)
repo_provider = RepositoryProviderMiddleware(
    {
        "user_repository": UserRepository,
        "job_vacancy_repository": JobVacancyRepository,
        "channel_repository": ChannelRepository,
    }
)

new_jobs_notifications = NewJobsNotifications(sessionmaker)

i18n_middleware = I18nMiddleware(
    core=FluentRuntimeCore(
        path=Path(__file__).resolve().parent.joinpath("locales"),
    ),
    default_locale="ru",
)
