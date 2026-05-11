import re
from datetime import datetime, timedelta
from types import SimpleNamespace

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid, UserNotParticipant
from pyrogram.handlers import MessageHandler
from pyrogram.types import ChatPermissions, Message

import config
from DAXXMUSIC import app
from DAXXMUSIC.misc import SUDOERS
from config import BANNED_USERS


ACTION_PATTERNS = (
    ("unmute", ("unmute", "wapas bolne do", "bolne do")),
    ("unban", ("unban", "wapas lao", "unblock")),
    ("mute", ("mute", "silent", "silence", "chup", "bolne mat do")),
    ("kick", ("kick", "remove", "hata", "nikal", "bahar")),
    ("warn", ("warn", "warning", "chetavni")),
    ("ban", ("ban", "banned", "block", "blacklist")),
)


def _has_wake_word(text):
    return any(re.search(rf"(?<!\w){re.escape(word)}(?!\w)", text) for word in config.WAKE_WORDS)


def _detect_action(text):
    for action, patterns in ACTION_PATTERNS:
        if any(pattern in text for pattern in patterns):
            return action
    return None


def _mute_duration(text):
    if "kal tak" in text:
        return timedelta(days=1)

    match = re.search(r"(\d+)\s*(min|mins|minute|minutes|m)\b", text)
    if match:
        return timedelta(minutes=int(match.group(1)))

    match = re.search(r"(\d+)\s*(hour|hours|hr|hrs|h)\b", text)
    if match:
        return timedelta(hours=int(match.group(1)))

    return timedelta(hours=1)


async def _is_allowed(message):
    user_id = message.from_user.id if message.from_user else None
    if not user_id:
        return False
    if user_id == config.OWNER_ID or user_id in SUDOERS:
        return True
    try:
        member = await app.get_chat_member(message.chat.id, user_id)
    except Exception:
        return False
    return member.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR)


async def _bot_can_restrict(chat_id):
    try:
        member = await app.get_chat_member(chat_id, app.id)
    except Exception:
        return False
    return (
        member.status == ChatMemberStatus.ADMINISTRATOR
        and member.privileges
        and member.privileges.can_restrict_members
    )


async def _bot_is_admin(chat_id):
    try:
        member = await app.get_chat_member(chat_id, app.id)
    except Exception:
        return False
    return member.status == ChatMemberStatus.ADMINISTRATOR


async def _resolve_target(message):
    if message.reply_to_message and message.reply_to_message.from_user:
        return message.reply_to_message.from_user

    text = message.text or ""
    username = re.search(r"@([A-Za-z0-9_]{5,32})", text)
    if username:
        try:
            return await app.get_users(username.group(1))
        except Exception:
            return None

    user_id = re.search(r"(?<!\d)(\d{5,})(?!\d)", text)
    if user_id:
        target_id = int(user_id.group(1))
        try:
            return await app.get_users(target_id)
        except Exception:
            return SimpleNamespace(
                id=target_id,
                mention=f"[{target_id}](tg://user?id={target_id})",
            )

    return None


def _is_protected(user):
    return user.id in {config.OWNER_ID, app.id} or user.id in SUDOERS


async def _reply_and_stop(message, text):
    await message.reply_text(text)
    await message.stop_propagation()


async def natural_moderation(_, message: Message):
    if not message.from_user or message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        return

    text = (message.text or "").lower()
    if text.startswith(("/", "!", "%", ",", ".", "@", "#")):
        return
    if not _has_wake_word(text):
        return

    action = _detect_action(text)
    if not action:
        return

    if not await _is_allowed(message):
        return await _reply_and_stop(message, "❌ You don't have permission to do this.")

    target = await _resolve_target(message)
    if not target:
        return await _reply_and_stop(
            message,
            "❌ Please reply to a user's message, mention username, or provide user ID.",
        )

    if _is_protected(target):
        return await _reply_and_stop(message, "❌ You don't have permission to do this.")

    if action == "warn" and not await _bot_is_admin(message.chat.id):
        return await _reply_and_stop(message, "❌ I need admin permission to perform this action.")
    if action != "warn" and not await _bot_can_restrict(message.chat.id):
        return await _reply_and_stop(message, "❌ I need admin permission to perform this action.")

    try:
        if action == "ban":
            await app.ban_chat_member(message.chat.id, target.id)
            return await _reply_and_stop(message, "✅ User banned successfully.")

        if action == "kick":
            await app.ban_chat_member(message.chat.id, target.id)
            await app.unban_chat_member(message.chat.id, target.id)
            return await _reply_and_stop(message, "✅ User removed successfully.")

        if action == "mute":
            until_date = datetime.now() + _mute_duration(text)
            await app.restrict_chat_member(
                message.chat.id,
                target.id,
                ChatPermissions(),
                until_date,
            )
            return await _reply_and_stop(message, "✅ User muted successfully.")

        if action == "unmute":
            await app.restrict_chat_member(
                message.chat.id,
                target.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_send_polls=True,
                    can_add_web_page_previews=True,
                    can_invite_users=True,
                ),
            )
            return await _reply_and_stop(message, "✅ User unmuted successfully.")

        if action == "unban":
            await app.unban_chat_member(message.chat.id, target.id)
            return await _reply_and_stop(message, "✅ User unbanned successfully.")

        if action == "warn":
            await message.reply_text(f"⚠️ Warning sent to user.\n{target.mention}, please follow the group rules.")
            return await message.stop_propagation()

    except (ChatAdminRequired, UserAdminInvalid):
        return await _reply_and_stop(message, "❌ I need admin permission to perform this action.")
    except UserNotParticipant:
        return await _reply_and_stop(message, "❌ Please reply to a user's message, mention username, or provide user ID.")
    except Exception:
        return await _reply_and_stop(message, "❌ I need admin permission to perform this action.")


app.add_handler(
    MessageHandler(natural_moderation, filters.text & filters.group & ~BANNED_USERS),
    group=-1,
)
