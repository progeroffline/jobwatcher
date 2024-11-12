from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext
from bot.dependencies import settings, logger

router = Router(name="notify_users")


@router.message(Command("bot_enable"))
async def enable_bot_notifications(message: Message, i18n: I18nContext):
    logger.info(
        "Admin enable notifications, "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id}, "
        f"Message: {message.text}"
    )
    settings.noitify_users_about_new_vacancies = True
    await message.answer(i18n.get("enable_bot_notifications"))


@router.message(Command("bot_disable"))
async def disable_bot_notifications(message: Message, i18n: I18nContext):
    logger.info(
        "Admin disable notifications, "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id}, "
        f"Message: {message.text}"
    )
    settings.noitify_users_about_new_vacancies = False
    await message.answer(i18n.get("disable_bot_notifications"))
