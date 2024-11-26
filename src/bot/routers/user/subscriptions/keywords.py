from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InaccessibleMessage, Message
from aiogram_i18n import I18nContext

from bot.keyboards.user.callback_types import KeywordsSubscriptionsMenu, UserMenu
from bot.keyboards.user.callback_values import SubscriptionsMenuActions, UserMenuActions
from bot.keyboards.user import inline_keyboards
from bot.repositories.user import UserRepository
from bot.dependencies import logger


router = Router(name="by_keyword")


class LocalStates(StatesGroup):
    enter_keyword = State()


@router.callback_query(
    UserMenu.filter(F.action == UserMenuActions.SUBSCRIPTIONS_BY_KEYWORD)
)
async def enter_keyword(
    call: CallbackQuery,
    i18n: I18nContext,
    state: FSMContext,
    user_repository: UserRepository,
):
    if call.message is None or isinstance(call.message, InaccessibleMessage):
        return await call.answer()

    logger.info(
        "User opened keyword menu, "
        f"User ID: {call.from_user.id}, "  # type: ignore
        f"Username: {call.from_user.username}, "  # type: ignore
        f"Chat ID: {call.message.chat.id}, "
        f"Callback data: {call.data}"
    )

    user = await user_repository.get_user_by_id(call.from_user.id)
    if user is None:
        return
    await state.set_state(LocalStates.enter_keyword)
    await call.message.edit_text(
        i18n.get(
            "enter_keyword",
            keyword="Пусто"
            if user.subscribed_keyword is None or len(user.subscribed_keyword) == 0
            else user.subscribed_keyword,
        ),
        reply_markup=inline_keyboards.back_to_user_menu(),
    )


@router.callback_query(
    KeywordsSubscriptionsMenu.filter(F.action == SubscriptionsMenuActions.ERASE)
)
async def erase_keywords(
    call: CallbackQuery,
    i18n: I18nContext,
    user_repository: UserRepository,
):
    if call.message is None or isinstance(call.message, InaccessibleMessage):
        return await call.answer()

    logger.info(
        "User erase keywords menu, "
        f"User ID: {call.from_user.id}, "  # type: ignore
        f"Username: {call.from_user.username}, "  # type: ignore
        f"Chat ID: {call.message.chat.id}, "
        f"Callback data: {call.data}"
    )

    await user_repository.update(user_id=call.from_user.id, subscribed_keyword="")
    await call.message.edit_text(
        i18n.get("keyword_erased"),
        reply_markup=inline_keyboards.back_to_user_menu(),
    )


@router.message(LocalStates.enter_keyword)
async def save_user_keyword(
    message: Message,
    i18n: I18nContext,
    user_repository: UserRepository,
    state: FSMContext,
):
    logger.info(
        "User enterd new keyword, "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id}, "
        f"Message: {message.text}"
    )
    await user_repository.update(message.from_user.id, subscribed_keyword=message.text)  # type: ignore
    await message.answer(
        i18n.get("save_user_keyword"),
        reply_markup=inline_keyboards.menu(),
    )

    await state.clear()
