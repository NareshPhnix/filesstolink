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
            # Fetch all participants of the AUTH_CHANNEL
            participants = await TelegramBot.get_participants(AUTH_CHANNEL)

            # Check if the user is in the list
            if user_id not in [p.id for p in participants]:
                raise UserNotParticipantError

            # If the user is a member, send the welcome message
            await event.reply(
                message=WelcomeText % {'first_name': event.sender.first_name},
                buttons=[
                    [Button.url('Add to Channel', f'https://t.me/{BOT_USERNAME}')]
                ]
            )
            return  # Stop execution if user is already in channel

        except UserNotParticipantError:
            # If the user is not a member, send a join message
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
            [Button.url('Add to Channel', f'https://t.me/{BOT_USERNAME}')]
        ]
    )