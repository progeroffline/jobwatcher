from enum import StrEnum


class UserMenuActions(StrEnum):
    SUBSCRIPTIONS = "subscriptions"


class SubscriptionsMenuActions(StrEnum):
    ENABLE = "enable"
    DISABLE = "disable"
