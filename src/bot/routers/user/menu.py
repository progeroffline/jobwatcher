from aiogram import F, Router
from aiogram.types import CallbackQuery, InaccessibleMessage, Message
from aiogram_i18n import I18nContext
from bot.dependencies import logger
from bot.keyboards.user import inline_keyboards
from bot.keyboards.user.callback_types import UserMenu
from bot.keyboards.user.callback_values import UserMenuActions


router = Router(name="menu")


async def user_welcome_message(message: Message, i18n: I18nContext):
    logger.info(
        "User opened menu, "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id},  "
        f"Message: {message.text}"
    )
    await message.answer(
        i18n.get("welcome_message"),
        reply_markup=inline_keyboards.menu(),
    )


@router.callback_query(UserMenu.filter(F.action == UserMenuActions.BACK_TO_MENU))
async def back_to_menu(
    call: CallbackQuery,
    callback_data: UserMenu,
    i18n: I18nContext,
):
    if call.message is None or isinstance(call.message, InaccessibleMessage):
        return await call.answer()

    logger.info(
        "User back to menu, "
        f"User ID: {call.from_user.id}, "  # type: ignore
        f"Username: {call.from_user.username}, "  # type: ignore
        f"Chat ID: {call.message.chat.id},  "
        f"Callback data: {call.data}"
    )

    await call.message.edit_text(
        i18n.get("welcome_message"),
        reply_markup=inline_keyboards.menu(),
    )
