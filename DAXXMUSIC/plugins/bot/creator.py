from pyrogram import filters
from pyrogram.types import Message

import config
from DAXXMUSIC import app
from config import BANNED_USERS


CREATOR_QUESTIONS = (
    "who made you",
    "who created you",
    "tumhe kisne banaya",
    "kisne banaya",
    "owner kaun hai",
    "developer kaun hai",
    "abhay kaun hai",
)


def _caption():
    return (
        "👑 Meet My Creator\n\n"
        f"Ye hain {config.CREATOR_NAME} — {config.CREATOR_TITLE}.\n\n"
        "Inhone mujhe design aur develop kiya hai. "
        f"Main {config.BOT_NAME} hoon, ek AI DJ Music Bot 🎧🔥"
    )


@app.on_message(filters.text & ~BANNED_USERS)
async def creator_identity(_, message: Message):
    text = (message.text or "").lower()
    if not any(question in text for question in CREATOR_QUESTIONS):
        return

    if config.CREATOR_PHOTO_URL:
        return await message.reply_photo(
            photo=config.CREATOR_PHOTO_URL,
            caption=_caption(),
        )
    await message.reply_text(_caption())
