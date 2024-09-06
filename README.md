# YaM4Bot

This is a simple Telegram bot that allows you to share audio files from the Yandex Music platform in inline mode.

You can use this bot by tagging it in any chat and providing the song name or a link. Tapping one of the results will send it to the chat.

<details>
<summary>Motivation</summary>

The bot was made out of frustration: it was hard for me to share music with my friends since most of them use other streaming platforms (hence [song.link](https://song.link) is in the caption of every message - whoever you sent the track to will be able not only to listen to it in Telegram but also add it to their playlist on some other platform). 

There were other problems as well: hosted bots that solve similar problems exist, but I found them unstable - it is easier to host the bot myself since I also author a Telegram channel and post music very often.

</details>

This bot is not affiliated with the Yandex Music project.

## Quick start

### Prerequisites

To run this bot, you will need:

- A valid Telegram Bot token. You can get one from [BotFather](https://t.me/BotFather).
  - you will need to create a new bot and use `/setinline` and `/setinlinefeedback` commands to set up inline mode
- A valid Yandex Music authentication token. You can get one using [this guide](https://yandex-music.readthedocs.io/en/main/token.html).
  - Note that some features (such as downloads with 320kbit/s bitrate) are only available to the Plus subscribers.
- A pre-made "dump chat" that will be used to upload audio files to Telegram (needed due to `aiogram` limitations). Create a private group, invite your bot to it and determine the chat ID using [one of these options](https://gist.github.com/mraaroncruz/e76d19f7d61d59419002db54030ebe35)

After gathering the information, clone the repo and place the tokens in an `./.env` file in the root directory of your project, similar to the example below:

```bash
TG_TOKEN="some:text"
YAM_TOKEN="y0_other_text"
DUMP_CHAT_ID="-000000000"
```

### Run using Docker

```bash
docker compose build
docker compose up
```

### Run on host

```bash
python3 -m venv .venv
source .venv/bin/activate # or .venv/Scripts/activate on Windows
pip install -r requirements.txt
python bot.py
```

## Credits
[Mukcep's YaM4Bot](https://github.com/Mukcep/yam4bot) - this was a starting point for my project (although I ended up fully rewriting it)

[@MarshalX's yandex-music-api](https://github.com/MarshalX/YandexMusic) - the library that made this possible

[aiogram](https://github.com/aiogram/aiogram) - another library that made this possible (although I'm not entirely happy with the file upload handling of this lib, I might try Telethon later)
