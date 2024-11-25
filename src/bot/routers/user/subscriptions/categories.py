from aiogram import Router, F
from aiogram.types import CallbackQuery, InaccessibleMessage
from aiogram_i18n import I18nContext
from bot.keyboards.user.callback_types import CategorySubscriptionsMenu, UserMenu
from bot.keyboards.user.callback_values import UserMenuActions, SubscriptionsMenuActions
from bot.keyboards.user import inline_keyboards
from bot.repositories.job_vacancy import JobVacancyRepository
from bot.repositories.user import UserRepository
from bot.dependencies import logger
from aiogram.exceptions import TelegramBadRequest


router = Router(name="by_categories")


@router.callback_query(
    UserMenu.filter(F.action == UserMenuActions.SUBSCRIPTIONS_BY_CATEGORY)
)
async def categories_menu(
    call: CallbackQuery,
    user_repository: UserRepository,
    job_vacancy_repository: JobVacancyRepository,
    i18n: I18nContext,
):
    if call.message is None or isinstance(call.message, InaccessibleMessage):
        return await call.answer()
    logger.info(
        "User opened categories menu, "
        f"User ID: {call.from_user.id}, "  # type: ignore
        f"Username: {call.from_user.username}, "  # type: ignore
        f"Chat ID: {call.message.chat.id}, "
        f"Callback data: {call.data}"
    )

    categories = await job_vacancy_repository.get_categories()
    subscriptions = await user_repository.get_category_subscriptions(call.from_user.id)
    await call.message.edit_text(
        i18n.get("subscriptions_menu"),
        reply_markup=inline_keyboards.categories_menu(categories, subscriptions),
    )


@router.callback_query(CategorySubscriptionsMenu.filter())
async def toggle_user_subscription_to_category(
    call: CallbackQuery,
    callback_data: CategorySubscriptionsMenu,
    user_repository: UserRepository,
    job_vacancy_repository: JobVacancyRepository,
    i18n: I18nContext,
):
    if call.message is None or isinstance(call.message, InaccessibleMessage):
        return await call.answer()

    logger.info(
        "User updated subscriptions category list, "
        f"User ID: {call.from_user.id}, "  # type: ignore
        f"Username: {call.from_user.username}, "  # type: ignore
        f"Chat ID: {call.message.chat.id}, "
        f"Callback data: {call.data}"
    )

    category = await job_vacancy_repository.get_category(id=callback_data.id)
    categories = await job_vacancy_repository.get_categories()
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
    elif callback_data.action == SubscriptionsMenuActions.ENABLE_ALL:
        await user_repository.enable_subscription_to_category(
            call.from_user.id,
            categories=categories,
        )
    elif callback_data.action == SubscriptionsMenuActions.DISABLE_ALL:
        await user_repository.disable_subscription_to_category(call.from_user.id)

    subscriptions = await user_repository.get_category_subscriptions(call.from_user.id)

    try:
        await call.message.edit_text(
            i18n.get("subscriptions_menu"),
            reply_markup=inline_keyboards.categories_menu(categories, subscriptions),
        )
    except TelegramBadRequest:
        await call.answer()
