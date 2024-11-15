from typing import Sequence
from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.user.callback_types import SubscriptionsMenu, UserMenu
from bot.keyboards.user.callback_values import SubscriptionsMenuActions, UserMenuActions
from bot.database.models.job_vacancy_categories import JobVacancyCategory
from bot.dependencies import settings


def menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=LazyProxy("subscriptions"),
                    callback_data=UserMenu(action=UserMenuActions.SUBSCRIPTIONS).pack(),
                ),
            ],
        ],
    )


def subscriptions_menu(
    categories: Sequence[JobVacancyCategory],
    subscriptions: Sequence[JobVacancyCategory],
) -> InlineKeyboardMarkup:
    inline_keyboard = []

    for category in categories:
        user_subscribed = category not in subscriptions

        text = (
            category.name
            if user_subscribed
            else f"{settings.selected_category_char} {category.name}"
        )
        action = (
            SubscriptionsMenuActions.ENABLE
            if user_subscribed
            else SubscriptionsMenuActions.DISABLE
        )

        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data=SubscriptionsMenu(
                        id=category.id,
                        action=action,
                    ).pack(),
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
