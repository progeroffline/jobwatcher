from aiogram import Router
from .keywords import router as keywords_router
from .categories import router as categories_router

router = Router(name="subscriptions")
router.include_router(keywords_router)
router.include_router(categories_router)
