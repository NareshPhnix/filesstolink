from telethon import Button
from telethon.events import NewMessage
from telethon.tl.custom.message import Message
from telethon.errors import ChatAdminRequiredError, UserNotParticipantError
from bot import TelegramBot
from bot.config import Telegram
from bot.modules.static import *
from bot.modules.decorators import verify_user

# Your channel username (without @)
CHANNEL_USERNAME = "filetolinkks"

@TelegramBot.on(NewMessage(incoming=True, pattern=r'^/start$'))
@verify_user(private=True)
async def welcome(event: NewMessage.Event | Message):
    user_id = event.sender_id

    try:
        # Check if the user is a member of the required channel
        participant = await TelegramBot.get_participant(CHANNEL_USERNAME, user_id)

        # If the user is a member, send the welcome message
        await event.reply(
            message=WelcomeText % {'first_name': event.sender.first_name},
            buttons=[
                [
                    Button.url('Add to Channel', f'https://t.me/{CHANNEL_USERNAME}')
                ]
            ]
        )

    except (UserNotParticipantError, ValueError):
        # If the user is not a member, send a join message
        await event.reply(
            "🚀 To use this bot, you must join our channel first:\n\n"
            f"👉 [Join Now](https://t.me/{CHANNEL_USERNAME})",
            buttons=[
                [Button.url("📢 Join Channel", f"https://t.me/{CHANNEL_USERNAME}")]
            ]
        )