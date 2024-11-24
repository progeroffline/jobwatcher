from aiogram import Router

from .menu import router as menu_router
from .subscriptions import router as subscriptions_router
from .search_by_keyword import router as search_by_keyword_router


router = Router(name="user")
router.include_router(menu_router)
router.include_router(subscriptions_router)
router.include_router(search_by_keyword_router)
