from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from DAXXMUSIC import app
from config import BOT_USERNAME, OWNER_ID, SUPPORT_CHANNEL, SUPPORT_CHAT
from DAXXMUSIC.utils.errors import capture_err
import httpx 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_txt = """**
✪ RUdexAbhay Music ✪

➲ AI DJ music bot for Telegram voice chats.
➲ Supports Render, AWS VPS, and Docker deployment.
➲ Owner: Abhay
**"""




@app.on_message(filters.command("nope"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("𝗔𝗗𝗗 𝗠𝗘", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
          InlineKeyboardButton("𝗛𝗘𝗟𝗣", url=SUPPORT_CHAT),
          InlineKeyboardButton("𝗢𝗪𝗡𝗘𝗥", user_id=OWNER_ID),
          ],
               [
                InlineKeyboardButton("CHANNEL", url=SUPPORT_CHANNEL),

],
[
              InlineKeyboardButton("SUPPORT", url=SUPPORT_CHAT),
              ],
              [
              InlineKeyboardButton("𝗠𝗔𝗡𝗔𝗚𝗘𝗠𝗘𝗡𝗧︎", url=SUPPORT_CHAT),
InlineKeyboardButton("𝗖𝗛𝗔𝗧 𝗕𝗢𝗧", url=SUPPORT_CHAT),
],
[
InlineKeyboardButton("BOT LIST", url=SUPPORT_CHAT),
],
[
              InlineKeyboardButton("𝗩𝗣𝗦", url=SUPPORT_CHAT),
              InlineKeyboardButton("𝗠𝗢𝗩𝗜𝗘︎", url=f"https://t.me/okflix_tg"),
              ],
[
InlineKeyboardButton("SUPPORT GROUP", url=SUPPORT_CHAT),

        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://telegra.ph/file/692c17cc052a9249b182a.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )
 
   
# --------------


@app.on_message(filters.command("repo", prefixes="#"))
@capture_err
async def repo(_, message):
    async with httpx.AsyncClient() as client:
        response = await client.get(SUPPORT_CHAT)
    
    if response.status_code == 200:
        users = response.json()
        list_of_users = ""
        count = 1
        for user in users:
            list_of_users += f"{count}. [{user['login']}]({user['html_url']})\n"
            count += 1

        text = f"""[RUdexAbhay Music]({SUPPORT_CHANNEL}) | [Support]({SUPPORT_CHAT})
| 𝖢𝖮𝖭𝖳𝖱𝖨𝖡𝖴𝖳𝖮𝖱𝖲 |
----------------
{list_of_users}"""
        await app.send_message(message.chat.id, text=text, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, text="Failed to fetch contributors.")
