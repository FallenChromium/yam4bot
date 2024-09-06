import logging
import hashlib
import re
import sys
import asyncio
import db
import yamusic
import config


from aiogram import Bot, Dispatcher
from aiogram.types import (
    FSInputFile,
    InlineQuery,
    Message,
    ChosenInlineResult,
    InlineQueryResultAudio,
    URLInputFile,
)
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import InputMediaAudio
from aiogram.filters import Command

TOKEN = config.TG_TOKEN

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=TOKEN)
dp = Dispatcher()
result_ids = {}  # Hash array Result_ID => Track_Id


def get_loading_markup(track_id: str | int):
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [InlineKeyboardButton(text="Загружаем...", callback_data=str(track_id))]
        ],
    )


def ymtrack_as_inline_result(
    track: yamusic.YandexTrack,
    result_id: str | None = None,
    markup: InlineKeyboardMarkup | None = None,
) -> InlineQueryResultAudio:
    result_id = (
        result_id or hashlib.md5(str(track.yandex_track_id).encode()).hexdigest()
    )
    result_ids[result_id] = track.yandex_track_id
    return InlineQueryResultAudio(
        id=result_id,
        # getting actual download link is slow and hurts the UX, so a placeholder is used
        audio_url="https://cs12.spac.me/f/022155028048118178004245225041194015065048227225162088184137/1651935767/90406904/0/912c9cca2ba0f5da4d0df7cb4f7483ea/placeholder-spcs.me.mp3#asdasd",
        title=track.title,
        performer=track.artists,
        audio_duration=track.duration,
        # reply markup is required to have ability to edit the message later on
        reply_markup=get_loading_markup(track.yandex_track_id),
    )


@dp.message(Command(commands="upload_placeholder"))
async def upload_placeholder(message: Message):
    result = await message.reply_audio(FSInputFile("./tagmp3_crank-2.mp3"))
    await message.reply(result.audio.file_id)


@dp.inline_query()
async def inline_search_audio(inline_query: InlineQuery):
    items = []
    query = inline_query.query

    if not query:
        pass
    elif query.startswith("https://"):
        # single-result mode
        yandex_match = re.match(
            r"https://music.yandex.(ru|by|kz|com)/album/(\d+)/track/(\d+)", query
        )
        if yandex_match:
            album_id, track_id = yandex_match.group(2), yandex_match.group(3)
            full_id = f"{track_id}:{album_id}"
            track = yamusic.get_track_data(full_id)
            items.append(ymtrack_as_inline_result(track))
    else:
        result = yamusic.search(query=query)

        items = [ymtrack_as_inline_result(track) for track in result[:20]]

    await bot.answer_inline_query(inline_query.id, results=items, cache_time=5)


@dp.chosen_inline_result()
async def chosen_track(chosen_inline_result: ChosenInlineResult):
    result_id = chosen_inline_result.result_id
    if result_id in result_ids:
        track_id = result_ids[result_id]
        track = db.get(track_id)
        tg_file_id = str(track.tg_file_id) if track else None
        data = yamusic.get_track_data(track_id)
        logging.info(f"Got data: {data}")
        if not tg_file_id:
            # it could be that using URLInputFile will get throttled by Yandex Music, but it hasn't been the case
            # In the event this does happen, it's safer to use FSInputFile

            # can't edit message and upload a file at the same time, pre-upload is required
            # aiogram doesn't support uploading without sending atm. A dummy chat has to be created and configured
            file = await bot.send_audio(
                audio=URLInputFile(data.get_download_link()),
                title=data.title,
                performer=str(data.artists),
                thumbnail=URLInputFile(data.cover_url),
                duration=data.duration,
                chat_id=config.DUMP_CHAT_ID,
            )

            tg_file_id = file.audio.file_id
            db.save(track_id, tg_file_id)

        await bot.edit_message_media(
            media=InputMediaAudio(
                media=tg_file_id,
                title=data.title,
                performer=str(data.artists),
                thumbnail=URLInputFile(data.cover_url),
                duration=data.duration,
            ),
            inline_message_id=chosen_inline_result.inline_message_id,
        )
        await bot.edit_message_caption(
            inline_message_id=chosen_inline_result.inline_message_id,
            caption=f"<a href='{data.link}'>Yandex Music</a>\n<a href='{f'odesli.co/{data.link}'}'>song.link</a>",
            parse_mode="HTML",
        )
    else:
        raise ("Unknown result id")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
