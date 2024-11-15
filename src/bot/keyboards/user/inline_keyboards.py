from itertools import zip_longest
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

    for pair in zip_longest(*[iter(categories)] * 2):
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=(
                        f"{settings.selected_category_char} {cat.name}"
                        if cat in subscriptions
                        else cat.name
                    ),
                    callback_data=SubscriptionsMenu(
                        id=cat.id,
                        action=(
                            SubscriptionsMenuActions.DISABLE
                            if cat in subscriptions
                            else SubscriptionsMenuActions.ENABLE
                        ),
                    ).pack(),
                )
                for cat in pair
                if cat is not None
            ]
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=LazyProxy("subscriptions_enable_all"),
                callback_data=SubscriptionsMenu(
                    id=1,
                    action=SubscriptionsMenuActions.ENABLE_ALL,
                ).pack(),
            ),
            InlineKeyboardButton(
                text=LazyProxy("subscriptions_disable_all"),
                callback_data=SubscriptionsMenu(
                    id=1,
                    action=SubscriptionsMenuActions.DISABLE_ALL,
                ).pack(),
            ),
        ],
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=LazyProxy("back_to_user_menu"),
                callback_data=UserMenu(
                    action=UserMenuActions.BACK_TO_MENU,
                ).pack(),
            ),
        ],
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
