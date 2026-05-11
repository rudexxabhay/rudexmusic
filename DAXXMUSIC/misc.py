import time

from pyrogram import filters

import config
from DAXXMUSIC.core.mongo import mongodb

from .logging import LOGGER

SUDOERS = filters.user()

_boot_ = time.time()


def dbb():
    global db
    db = {}
    LOGGER(__name__).info("RUdexAbhay Music database cache loaded.")


async def sudo():
    global SUDOERS
    SUDOERS.add(config.OWNER_ID)
    for user_id in config.SUDO_USERS:
        SUDOERS.add(user_id)
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    if config.OWNER_ID not in sudoers:
        sudoers.append(config.OWNER_ID)
    for user_id in config.SUDO_USERS:
        if user_id not in sudoers:
            sudoers.append(user_id)
    if sudoers:
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudoers}},
            upsert=True,
        )
    if sudoers:
        for user_id in sudoers:
            SUDOERS.add(user_id)
    LOGGER(__name__).info("RUdexAbhay Music sudo users loaded.")
