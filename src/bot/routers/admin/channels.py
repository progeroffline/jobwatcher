from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router(name="channels")


@router.message(Command("channels"))
async def channels(message: Message): ...


@router.message(Command("channels_remove"))
async def channels_remove(message: Message): ...


@router.message(Command("channels_add"))
async def channels_add(message: Message): ...


@router.message(Command("channels_time"))
async def channels_time(message: Message): ...
