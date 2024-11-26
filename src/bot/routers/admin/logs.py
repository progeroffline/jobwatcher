from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from aiogram_i18n import I18nContext
from bot.dependencies import settings
from bot.dependencies import logger


router = Router(name="logs")


@router.message(Command("logs"))
async def get_logs(message: Message, i18n: I18nContext):
    logger.info(
        "Admin got log file, "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id}, "
    )

    await message.answer_document(
        caption=i18n.get("log_file_sent"),
        document=FSInputFile(settings.logger_logfile_path),
    )
