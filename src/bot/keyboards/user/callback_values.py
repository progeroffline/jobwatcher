from enum import StrEnum


class UserMenuActions(StrEnum):
    SUBSCRIPTIONS_BY_CATEGORY = "subscriptions_by_category"
    SUBSCRIPTIONS_BY_KEYWORD = "subscriptions_by_keyword"
    SUBSCRIPTIONS_BY_REGION = "subscriptions_by_region"
    BACK_TO_MENU = "back_to_menu"


class SubscriptionsMenuActions(StrEnum):
    ENABLE = "enable"
    DISABLE = "disable"
    ENABLE_ALL = "enable_all"
    DISABLE_ALL = "disable_all"
