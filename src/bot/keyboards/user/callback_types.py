from aiogram.filters.callback_data import CallbackData
from bot.keyboards.user.callback_values import SubscriptionsMenuActions, UserMenuActions


class UserMenu(CallbackData, prefix="user"):
    action: UserMenuActions


class CategorySubscriptionsMenu(CallbackData, prefix="category_subscriptions_menu"):
    id: int
    action: SubscriptionsMenuActions


class RegionSubscriptionsMenu(CallbackData, prefix="region_subscriptions_menu"):
    region: str
    action: SubscriptionsMenuActions


class KeywordsSubscriptionsMenu(CallbackData, prefix="keywords_subscriptions_menu"):
    action: str
