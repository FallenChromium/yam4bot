import logging
import re

from mutagen.flac import FLAC, Picture
from mutagen.id3 import APIC, ID3, TALB, TDRC, TIT2, TPE1
from mutagen.mp4 import MP4, MP4Cover


def detect_format(data: bytes) -> str:
    if data[:4] == b"fLaC":
        return "flac"
    if data[:3] == b"ID3" or (
        len(data) > 2 and data[0] == 0xFF and (data[1] & 0xE0) == 0xE0
    ):
        return "mp3"
    if data[4:8] == b"ftyp":
        return "m4a"
    logging.warning("Unknown audio format, assuming m4a")
    return "m4a"


def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|\r\n\t]+', " ", name).strip(" .")[:120]


def tag(
    path: str,
    fmt: str,
    title: str,
    artists: str,
    album: str | None = None,
    year: int | None = None,
    cover: bytes | None = None,
):
    if fmt == "mp3":
        tags = ID3()
        tags.add(TIT2(encoding=3, text=title))
        tags.add(TPE1(encoding=3, text=artists))
        if album:
            tags.add(TALB(encoding=3, text=album))
        if year:
            tags.add(TDRC(encoding=3, text=str(year)))
        if cover:
            tags.add(
                APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=cover)
            )
        tags.save(path)
    elif fmt == "flac":
        tags = FLAC(path)
        tags["title"] = [title]
        tags["artist"] = [artists]
        if album:
            tags["album"] = [album]
        if year:
            tags["date"] = [str(year)]
        if cover:
            pic = Picture()
            pic.type = 3
            pic.mime = "image/jpeg"
            pic.data = cover
            tags.add_picture(pic)
        tags.save()
    else:  # m4a
        tags = MP4(path)
        tags["\xa9nam"] = [title]
        tags["\xa9ART"] = [artists]
        if album:
            tags["\xa9alb"] = [album]
        if year:
            tags["\xa9day"] = [str(year)]
        if cover:
            tags["covr"] = [MP4Cover(cover, imageformat=MP4Cover.FORMAT_JPEG)]
        tags.save()
