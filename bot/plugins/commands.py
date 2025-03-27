from telethon import Button
from telethon.events import NewMessage
from telethon.tl.custom.message import Message
from telethon.errors import UserNotParticipantError
from bot import TelegramBot
from bot.config import Telegram, AUTH_CHANNEL
from bot.modules.static import *
from bot.modules.decorators import verify_user

@TelegramBot.on(NewMessage(incoming=True, pattern=r'^/start$'))
@verify_user(private=True)
async def welcome(event: NewMessage.Event | Message):
    user_id = event.sender_id

    if AUTH_CHANNEL:
        try:
            # Check if user is a member of the AUTH_CHANNEL
            participant = await TelegramBot.get_participant(AUTH_CHANNEL, user_id)

            # If user is a member, send the welcome message
            await event.reply(
                message=WelcomeText % {'first_name': event.sender.first_name},
                buttons=[
                    [Button.url('Add to Channel', f'https://t.me/{Telegram.BOT_USERNAME}')]
                ]
            )
            return  # Stop execution if user is already in channel

        except UserNotParticipantError:
            # If user is not a member, send a join message
            await event.reply(
                "🚀 To use this bot, please join our channel first:\n\n"
                f"👉 [Join Now](https://t.me/{AUTH_CHANNEL})",
                buttons=[
                    [Button.url("📢 Join Channel", f"https://t.me/{AUTH_CHANNEL}")]
                ]
            )
            return  # Stop execution if user is not in the channel

    # If AUTH_CHANNEL is not set, proceed normally
    await event.reply(
        message=WelcomeText % {'first_name': event.sender.first_name},
        buttons=[
            [Button.url('Add to Channel', f'https://t.me/{Telegram.BOT_USERNAME}')]
        ]
    )