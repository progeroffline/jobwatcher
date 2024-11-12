from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext
from bot.dependencies import logger


router = Router(name="menu")


@router.message(Command("admin"))
async def admin_menu(message: Message, i18n: I18nContext):
    logger.info(
        "Admin opened admin menu, "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id},  "
        f"Message: {message.text}"
    )
    await message.answer(text=i18n.get("admin_menu"))
