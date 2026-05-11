from html import unescape
from urllib.parse import quote_plus

import aiohttp
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from DAXXMUSIC import app


def _search_keyboard(results):
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(title[:64] or "Open result", url=url)]
            for title, url in results[:5]
            if url
        ]
    )


@app.on_message(filters.command("google"))
async def search_(_, msg: Message):
    split = msg.text.split(None, 1)
    if len(split) == 1:
        return await msg.reply_text("**Give a query to search.**")

    query = split[1].strip()
    url = f"https://www.google.com/search?q={quote_plus(query)}"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Open Google results", url=url)]]
    )
    await msg.reply_text(
        f"**Search results for:** `{query}`",
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


@app.on_message(filters.command("stack"))
async def stack_search_(_, msg: Message):
    split = msg.text.split(None, 1)
    if len(split) == 1:
        return await msg.reply_text("**Give a query to search.**")

    query = split[1].strip()
    status = await msg.reply_text("**Searching Stack Overflow...**")
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.stackexchange.com/2.3/search/advanced",
                params=params,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                data = await response.json()

        results = [
            (unescape(item.get("title", "Stack Overflow result")), item.get("link"))
            for item in data.get("items", [])
        ]
        if not results:
            await status.delete()
            return await msg.reply_text("**No Stack Overflow results found.**")

        await status.delete()
        await msg.reply_text(
            f"**Stack Overflow results for:** `{query}`",
            reply_markup=_search_keyboard(results),
            disable_web_page_preview=True,
        )
    except Exception as exc:
        await status.delete()
        await msg.reply_text("**Search failed. Please try again later.**")
        print(f"stack search error: {exc}")
