from enum import StrEnum


class UserMenuActions(StrEnum):
    SUBSCRIPTIONS = "subscriptions"
    BACK_TO_MENU = "back_to_menu"


class SubscriptionsMenuActions(StrEnum):
    ENABLE = "enable"
    DISABLE = "disable"
    ENABLE_ALL = "enable_all"
    DISABLE_ALL = "disable_all"
