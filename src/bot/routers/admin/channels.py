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
from bot.dependencies import logger


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
    logger.info(
        "Admin opened channels menu, "
        f"User ID: {message.from_user.id},"  # type: ignore
        f"Username: {message.from_user.username},"  # type: ignore
        f"Chat ID: {message.chat.id}, "
        f"Message: {message.text}"
    )
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
    logger.info(
        "Admin remove channel menu, "
        f"User ID: {message.from_user.id},"  # type: ignore
        f"Username: {message.from_user.username},"  # type: ignore
        f"Chat ID: {message.chat.id}, "
        f"Message: {message.text}"
    )
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

    logger.info(
        "Admin received channel message to remove, "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id}, "
        f"Message: {message.text}, "
        f"Channel ID: {channel.id}, "
        f"Channel Title: {channel.title}"
    )

    await channel_repository.delete(id=channel.id)
    await message.answer(i18n.get("success_remove_channel_to_database"))
    await state.clear()

    logger.info(
        "Channel successfully remove by admin request, "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id}, "
        f"Message: {message.text}, "
        f"Channel ID: {channel.id}, "
        f"Channel Title: {channel.title}"
    )


@router.message(Command("channels_add"))
async def channels_add(message: Message, i18n: I18nContext, state: FSMContext):
    logger.info(
        "Admin opened add channel menu, "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id}, "
        f"Message: {message.text}, "
    )

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

    logger.info(
        "Admin received channel message to add, "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id}, "
        f"Message: {message.text}, "
        f"Channel ID: {channel.id}, "
        f"Channel Title: {channel.title}"
    )

    if not await channel_repository.exists(channel.id):  # type: ignore
        await channel_repository.create(id=channel.id, title=channel.title)
        await message.answer(i18n.get("success_save_channel_to_database"))
        await state.clear()

        logger.info(
            "Channel successfully add by admin request, "
            f"User ID: {message.from_user.id}, "  # type: ignore
            f"Username: {message.from_user.username}, "  # type: ignore
            f"Chat ID: {message.chat.id}, "
            f"Message: {message.text}, "
            f"Channel ID: {channel.id}, "
            f"Channel Title: {channel.title}"
        )
    else:
        await message.answer(i18n.get("channel_already_added"))
        logger.info(
            "Channel add failed cause channel already exists in database, "
            f"User ID: {message.from_user.id}, "  # type: ignore
            f"Username: {message.from_user.username}, "  # type: ignore
            f"Chat ID: {message.chat.id}, "
            f"Message: {message.text}, "
            f"Channel ID: {channel.id}, "
            f"Channel Title: {channel.title}"
        )


@router.message(Command("channels_time"))
async def channels_time(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
):
    logger.info(
        "Admin opened channel update time menu, "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id}, "
        f"Message: {message.text}, "
    )
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

    logger.info(
        "Admin received channel message to update time, "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id}, "
        f"Message: {message.text}, "
        f"Channel ID: {channel.id}, "
        f"Channel Title: {channel.title}"
    )
    if not await channel_repository.exists(channel.id):  # type: ignore
        logger.info(
            "Admin update time failed channel not exists in database, "
            f"User ID: {message.from_user.id}, "  # type: ignore
            f"Username: {message.from_user.username}, "  # type: ignore
            f"Chat ID: {message.chat.id}, "
            f"Message: {message.text}, "
            f"Channel ID: {channel.id}, "
            f"Channel Title: {channel.title}"
        )
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

    logger.info(
        "Admin update channel time , "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id}, "
        f"Message: {message.text}, "
        f"Channel ID: {data['channel_id']}"
    )

    data = await state.get_data()
    await channel_repository.update(int(data["channel_id"]), post_interval=message.text)
    await message.answer(i18n.get("channel_post_interval_updated"))
    await state.clear()

    logger.info(
        "Admin successfully updated channel time , "
        f"User ID: {message.from_user.id}, "  # type: ignore
        f"Username: {message.from_user.username}, "  # type: ignore
        f"Chat ID: {message.chat.id}, "
        f"Message: {message.text}, "
        f"Channel ID: {data['channel_id']}"
    )
