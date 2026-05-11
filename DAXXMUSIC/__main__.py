import asyncio
import importlib

from aiohttp import web
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from DAXXMUSIC import LOGGER, app, userbot
from DAXXMUSIC.core.call import DAXX
from DAXXMUSIC.misc import sudo
from DAXXMUSIC.plugins import ALL_MODULES
from DAXXMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def _health_check(_):
    return web.Response(text="RUdexAbhay Music is running")


async def _start_web_server():
    app_server = web.Application()
    app_server.router.add_get("/", _health_check)
    app_server.router.add_get("/health", _health_check)
    runner = web.AppRunner(app_server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", config.PORT)
    await site.start()
    LOGGER("RUdexAbhay Music").info(f"Health server started on port {config.PORT}.")
    return runner


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐒𝐞𝐬𝐬𝐢𝐨𝐧")
        exit()
    web_runner = await _start_web_server()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("DAXXMUSIC.plugins" + all_module)
    LOGGER("RUdexAbhay Music plugins").info("RUdexAbhay Music features loaded.")
    await userbot.start()
    await DAXX.start()
    try:
        await DAXX.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("RUdexAbhay Music").error(
            "Please start your log group/channel voice chat. RUdexAbhay Music stopped."
        )
        exit()
    except:
        pass
    await DAXX.decorators()
    LOGGER("RUdexAbhay Music").info("RUdexAbhay Music started. Owner: Abhay.")
    await idle()
    await app.stop()
    await userbot.stop()
    await web_runner.cleanup()
    LOGGER("RUdexAbhay Music").info("RUdexAbhay Music stopped.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
