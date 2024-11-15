from aiogram import Router, F
from aiogram.types import CallbackQuery, InaccessibleMessage
from aiogram_i18n import I18nContext
from bot.keyboards.user.callback_types import SubscriptionsMenu, UserMenu
from bot.keyboards.user.callback_values import UserMenuActions, SubscriptionsMenuActions
from bot.keyboards.user import inline_keyboards
from bot.repositories.job_vacancy import JobVacancyRepository
from bot.repositories.user import UserRepository
from bot.dependencies import logger


router = Router(name="subscriptions")


@router.callback_query(UserMenu.filter(F.action == UserMenuActions.SUBSCRIPTIONS))
async def subscriptions_menu(
    call: CallbackQuery,
    user_repository: UserRepository,
    job_vacancy_repository: JobVacancyRepository,
    i18n: I18nContext,
):
    if call.message is None or isinstance(call.message, InaccessibleMessage):
        return await call.answer()
    logger.info(
        "User opened subscriptions menu, "
        f"User ID: {call.from_user.id}, "  # type: ignore
        f"Username: {call.from_user.username}, "  # type: ignore
        f"Chat ID: {call.message.chat.id}, "
        f"CallbackData: {call.data}"
    )

    categories = await job_vacancy_repository.get_categories()
    subscriptions = await user_repository.get_subscriptions(call.from_user.id)
    await call.message.edit_text(
        i18n.get("subscriptions_menu"),
        reply_markup=inline_keyboards.subscriptions_menu(categories, subscriptions),
    )


@router.callback_query(SubscriptionsMenu.filter())
async def enable_user_subscription_to_category(
    call: CallbackQuery,
    callback_data: SubscriptionsMenu,
    user_repository: UserRepository,
    job_vacancy_repository: JobVacancyRepository,
    i18n: I18nContext,
):
    if call.message is None or isinstance(call.message, InaccessibleMessage):
        return await call.answer()

    logger.info(
        "User updated subscriptions list, "
        f"User ID: {call.from_user.id}, "  # type: ignore
        f"Username: {call.from_user.username}, "  # type: ignore
        f"Chat ID: {call.message.chat.id}, "
        f"CallbackData: {call.data}"
    )

    category = await job_vacancy_repository.get_category(id=callback_data.id)
    if callback_data.action == SubscriptionsMenuActions.ENABLE:
        await user_repository.enable_subscription_to_category(
            call.from_user.id,
            category,
        )
    elif callback_data.action == SubscriptionsMenuActions.DISABLE:
        await user_repository.disable_subscription_to_category(
            call.from_user.id,
            category,
        )

    categories = await job_vacancy_repository.get_categories()
    subscriptions = await user_repository.get_subscriptions(call.from_user.id)
    await call.message.edit_text(
        i18n.get("subscriptions_menu"),
        reply_markup=inline_keyboards.subscriptions_menu(categories, subscriptions),
    )
