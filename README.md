# RUdexAbhay Music

RUdexAbhay Music is a Telegram AI DJ Music Bot created and owned by Abhay. It plays music in Telegram voice chats, supports normal `/play` commands, and can understand simple natural language music requests.

## Features

- Telegram voice chat music playback.
- AI DJ style natural language music detection.
- Mood-based song search for sad, romantic, gym, study, coding, party, night, and alone requests.
- Creator identity response for Abhay.
- Owner and sudo admin access for protected commands.
- MongoDB-backed bot data.
- Render Web Service and AWS Ubuntu VPS deployment support.

## Natural Language Examples

Users can request music without `/play`:

```text
babu safar song baja do
baby romantic gana chalao
babu sad song lagao
```

The bot listens for wake words such as `babu`, `baby`, `dj`, `abhay`, and `bot`, then detects music intent words such as `play`, `song`, `gana`, `music`, `baja`, `chalao`, and `lagao`.

## Creator Identity

When someone asks `who made you`, `who created you`, `tumhe kisne banaya`, `kisne banaya`, `owner kaun hai`, `developer kaun hai`, or `abhay kaun hai`, the bot replies with Abhay's creator identity.

If `CREATOR_PHOTO_URL` is set, the bot sends the photo with this caption:

```text
👑 Meet My Creator

Ye hain Abhay — Software Engineer.

Inhone mujhe design aur develop kiya hai. Main RUdexAbhay Music hoon, ek AI DJ Music Bot 🎧🔥
```

If no photo URL is set, it sends the same content as text.

## Sudo And Admin

- `OWNER_ID` has full access.
- `SUDO_USERS` accepts comma-separated Telegram user IDs.
- Protected commands include restart, broadcast, stats, ban, unban, and global ban tools.
- Existing Telegram group admin behavior is preserved for normal group moderation commands.

## Natural Language Moderation

Owners, sudo users, and Telegram group admins can moderate users without slash commands. Use these by replying to a user's message, mentioning a username, or providing a numeric Telegram user ID.

Hindi/Hinglish examples:

```text
babu isse ban krdo
babu ise ban karo
baby isko group se hata do
babu is user ko nikal do
babu @username ko ban krdo
babu isko mute krdo
baby isse chup kara do
babu isko bolne mat do
babu isse unmute krdo
babu isko wapas bolne do
babu isko unban krdo
babu isko warning do
babu is user ko warn karo
```

English examples:

```text
babu ban this user
baby ban him
babu kick this user
babu remove this user
babu mute him
baby silence this user
babu unmute this user
babu unban this user
babu warn this user
babu give warning to @username
```

Casual Indian examples:

```text
babu isko bahar karo
babu isko group se bahar nikal do
baby ye spam kar raha hai isko mute karo
babu ye banda pareshaan kar raha hai ban karo
babu is member ko remove karo
babu faltu message kar raha hai mute karo
babu isko 10 min ke liye mute karo
babu isko 1 hour mute karo
babu isko kal tak mute karo
```

Mute duration supports `10 min`, `30 minutes`, `1 hour`, `2 hours`, and `kal tak`. If no duration is found, mute defaults to 1 hour.

## Required Environment Variables

Create a real `.env` file from `.env.example` before running the bot:

```bash
cp .env.example .env
```

Fill these values:

```env
API_ID=
API_HASH=
BOT_TOKEN=
BOT_USERNAME=
BOT_NAME=RUdexAbhay Music
OWNER_ID=
OWNER_USERNAME=Abhay
SUDO_USERS=
ASSUSERNAME=
SUPPORT_CHANNEL=
SUPPORT_CHAT=
STRING_SESSION=
MONGO_DB_URI=
LOGGER_ID=
PORT=8000
NODE_ENV=production
CREATOR_NAME=Abhay
CREATOR_TITLE=Software Engineer
CREATOR_PHOTO_URL=
CREATOR_BIO=Creator of RUdexAbhay Music Bot
```

Notes:

- Get `BOT_TOKEN` from Telegram `@BotFather`.
- Get `API_ID` and `API_HASH` from `https://my.telegram.org`.
- `STRING_SESSION` is required for the assistant account used in voice chats.
- `LOGGER_ID` must be a Telegram group/channel where the bot is admin.
- Do not commit `.env`; it contains secrets.

## Local Setup

1. Install Python 3.11 and `ffmpeg`. Python 3.11 is recommended for local testing. Python 3.12 can be used for dependency installation with `Pillow>=10.4.0`, but Python 3.11 is still the safest choice for Telegram voice-call packages.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Create `.env` from `.env.example`.
5. Start the bot.

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip setuptools wheel
pip install -r requirements.txt
python -m DAXXMUSIC
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
pip install -r requirements.txt
cp .env.example .env
python -m DAXXMUSIC
```

You can also use the npm wrapper:

```bash
npm start
```

## Render Deployment

Use a Render Web Service. The bot starts a small health endpoint on `PORT` so Render can keep the service alive.

1. Push this project to GitHub.
2. Create a new Web Service on Render.
3. Connect the GitHub repository.
4. Select Python environment.
5. Set the build command:

```bash
pip install -r requirements.txt
```

6. Set the start command:

```bash
python -m DAXXMUSIC
```

7. Add all required environment variables from `.env.example` in the Render dashboard.
8. Deploy.

Required Render env variables:

```env
API_ID=
API_HASH=
BOT_TOKEN=
BOT_USERNAME=
BOT_NAME=RUdexAbhay Music
OWNER_ID=
OWNER_USERNAME=Abhay
SUDO_USERS=
ASSUSERNAME=
SUPPORT_CHANNEL=
SUPPORT_CHAT=
STRING_SESSION=
MONGO_DB_URI=
LOGGER_ID=
PORT=8000
NODE_ENV=production
CREATOR_NAME=Abhay
CREATOR_TITLE=Software Engineer
CREATOR_PHOTO_URL=
CREATOR_BIO=Creator of RUdexAbhay Music Bot
```

Deployment files included for Render:

- `render.yaml`
- `runtime.txt`
- `apt.txt` for `ffmpeg`
- `Procfile`

## AWS Ubuntu VPS Deployment With pm2

Ubuntu 22.04 is recommended.

Install packages:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv ffmpeg git -y
```

Clone the project:

```bash
git clone <repo>
cd <repo>
```

Create environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -U pip setuptools wheel
pip install -r requirements.txt
```

Create `.env`, fill real values, then run once manually:

```bash
cp .env.example .env
nano .env
python3 -m DAXXMUSIC
```

PM2 setup:

```bash
sudo apt install nodejs npm -y
sudo npm install -g pm2
```

Run bot with pm2:

```bash
pm2 start "python3 -m DAXXMUSIC" --name rudexmusic
```

Auto restart:

```bash
pm2 save
pm2 startup
```

Useful commands:

```bash
pm2 logs rudexmusic
pm2 restart rudexmusic
pm2 stop rudexmusic
```

## Commands

- `/play <song name or url>` - play music.
- `/vplay <song name or url>` - play video.
- `/pause` - pause playback.
- `/resume` - resume playback.
- `/skip` - skip current track.
- `/stop` - stop playback.
- `/queue` - show queue.
- `/settings` - group playback settings.
- `/stats` or `/gstats` - sudo-only stats.
- `/broadcast <message>` - sudo-only broadcast.
- `/restart` - sudo-only restart.
- `/ban`, `/unban` - group admin commands; owner/sudo can also use them.
- `/gban`, `/ungban`, `/gbanlist` - sudo-only global ban tools.
- `/addsudo`, `/delsudo`, `/delallsudo` - owner-only sudo management.

Natural language moderation also supports ban, unban, mute, unmute, kick/remove, and warn actions without slash commands.

## Troubleshooting

- `String Session Not Filled`: add a valid `STRING_SESSION` to `.env`.
- Bot cannot access logger chat: add the bot to `LOGGER_ID` chat and promote it as admin.
- Music does not start: start a voice chat in the group/channel and make sure the assistant account can join.
- `ffmpeg` errors: install `ffmpeg` locally or use the Dockerfile.
- Pillow install errors on Windows, such as `Failed to build 'pillow'` or `KeyError: '__version__'`: run `pip install --only-binary=:all: "Pillow>=10.4.0"` and then run `pip install -r requirements.txt` again.
- `py-tgcalls` install errors: use Python 3.10 or 3.11, recreate `.venv`, then run `pip install -r requirements.txt` again.
- MongoDB errors: verify `MONGO_DB_URI`.
- Render deploy fails: use a Web Service, keep start command as `python -m DAXXMUSIC`, and make sure all env variables are set.
- Commands do not work for sudo users: verify `OWNER_ID` and comma-separated `SUDO_USERS` are numeric Telegram user IDs.
- Natural moderation says target is missing: reply to the target user's message, mention `@username`, or include the numeric user ID.
- Natural moderation says admin permission is needed: promote the bot with ban/restrict user permission.
