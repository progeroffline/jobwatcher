from enum import StrEnum


class UserMenuActions(StrEnum):
    SUBSCRIPTIONS = "subscriptions"


class SubscriptionsMenuActions(StrEnum):
    ENABLE = "enable"
    DISABLE = "disable"
    ENABLE_ALL = "enable_all"
    DISABLE_ALL = "disable_all"
