from aiogram.filters.callback_data import CallbackData
from bot.keyboards.user.callback_values import SubscriptionsMenuActions, UserMenuActions


class UserMenu(CallbackData, prefix="user"):
    action: UserMenuActions


class SubscriptionsMenu(CallbackData, prefix="subscriptions_menu"):
    id: int
    action: SubscriptionsMenuActions
