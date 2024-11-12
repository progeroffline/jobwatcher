from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    MessageOriginChat,
    MessageOriginHiddenUser,
    MessageOriginUser,
)
from aiogram_i18n import I18nContext

from bot.repositories.channel import ChannelRepository


router = Router(name="channels")


class LocalStates(StatesGroup):
    enter_channel_message_to_add = State()
    enter_channel_message_to_remove = State()
    enter_channel_message_to_update_time = State()
    enter_update_time = State()


@router.message(Command("channels"))
async def channels(
    message: Message,
    channel_repository: ChannelRepository,
    i18n: I18nContext,
    state: FSMContext,
):
    await state.clear()
    channels = await channel_repository.get_all()
    if len(channels) == 0:
        return await message.answer(i18n.get("channels_list_is_empty"))
    await message.answer(
        text="\n".join(
            [
                f"{channel.id} | {channel.title} | {channel.post_interval} ч."
                for channel in channels
            ],
        ),
    )


@router.message(Command("channels_remove"))
async def channels_remove(message: Message, i18n: I18nContext, state: FSMContext):
    await state.clear()
    await message.answer(i18n.get("enter_channel_message_to_remove"))
    await state.set_state(LocalStates.enter_channel_message_to_remove)


@router.message(LocalStates.enter_channel_message_to_remove)
async def remove_channel_from_database(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    channel_repository: ChannelRepository,
):
    if (
        isinstance(message.forward_origin, MessageOriginUser)
        or isinstance(message.forward_origin, MessageOriginHiddenUser)
        or isinstance(message.forward_from, MessageOriginChat)
    ):
        return

    channel = message.forward_origin.chat  # type: ignore
    await channel_repository.delete(id=channel.id)
    await message.answer(i18n.get("success_remove_channel_to_database"))
    await state.clear()


@router.message(Command("channels_add"))
async def channels_add(message: Message, i18n: I18nContext, state: FSMContext):
    await state.clear()
    await message.answer(i18n.get("enter_channel_message_to_add"))
    await state.set_state(LocalStates.enter_channel_message_to_add)


@router.message(LocalStates.enter_channel_message_to_add)
async def save_channel_to_database(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    channel_repository: ChannelRepository,
):
    if (
        isinstance(message.forward_origin, MessageOriginUser)
        or isinstance(message.forward_origin, MessageOriginHiddenUser)
        or isinstance(message.forward_from, MessageOriginChat)
    ):
        return

    channel = message.forward_origin.chat  # type: ignore
    if not await channel_repository.exists(channel.id):  # type: ignore
        await channel_repository.create(id=channel.id, title=channel.title)
        await message.answer(i18n.get("success_save_channel_to_database"))
        await state.clear()
    else:
        await message.answer(i18n.get("channel_already_added"))


@router.message(Command("channels_time"))
async def channels_time(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
):
    await state.clear()
    await message.answer(i18n.get("enter_channel_message_to_update_time"))
    await state.set_state(LocalStates.enter_channel_message_to_update_time)


@router.message(LocalStates.enter_channel_message_to_update_time)
async def enter_channel_message_to_update_time(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    channel_repository: ChannelRepository,
):
    if (
        isinstance(message.forward_origin, MessageOriginUser)
        or isinstance(message.forward_origin, MessageOriginHiddenUser)
        or isinstance(message.forward_from, MessageOriginChat)
    ):
        return
    channel = message.forward_origin.chat  # type: ignore
    if not await channel_repository.exists(channel.id):  # type: ignore
        return await message.answer(i18n.get("channel_not_found"))

    await state.update_data(channel_id=channel.id)
    await message.answer(i18n.get("enter_new_post_interval"))
    await state.set_state(LocalStates.enter_update_time)


@router.message(LocalStates.enter_update_time)
async def enter_update_time(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    channel_repository: ChannelRepository,
):
    if message.text is None:
        return
    if not message.text.isdigit():
        return

    data = await state.get_data()
    await channel_repository.update(int(data["channel_id"]), post_interval=message.text)
    await message.answer(i18n.get("channel_post_interval_updated"))
    await state.clear()
