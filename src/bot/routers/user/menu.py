from aiogram import Router
from aiogram.types import Message
from aiogram_i18n import I18nContext
from bot.dependencies import logger


router = Router(name="menu")


async def user_welcome_message(message: Message, i18n: I18nContext):
    logger.info(
        "User opened menu, "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id},  "
        f"Message: {message.text}"
    )
    await message.answer(i18n.get("welcome_message"))
