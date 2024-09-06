from dataclasses import dataclass
import logging
from typing import List
import config

from yandex_music import Client, Track as YMTrack

client = Client(config.YAM_TOKEN).init()


@dataclass
class Track:
    title: str
    artists: str
    link: str
    cover_url: str | None
    duration: int

    def get_download_link():
        pass


class YandexTrack(Track):
    yandex_track_id: str

    def __init__(self, track: YMTrack):
        super().__init__(**self.parse_from_ymtrack(track))
        self.yandex_track_id = track.id

    @classmethod
    def from_id(cls, track_id: str | int):
        track = client.tracks([track_id])[0]
        return cls(track)

    @classmethod
    def parse_from_ymtrack(cls, track: YMTrack):
        return {
            "title": track.title,
            "artists": ", ".join([artist.name for artist in track.artists]),
            "link": get_link(track.id),
            "cover_url": (
                "https://" + track.cover_uri.replace("%%", "400x400")
                if track.cover_uri
                else None
            ),
            "duration": int(track.duration_ms / 1000) if track.duration_ms else 0,
        }

    def get_download_link(self):
        track = client.tracks([self.yandex_track_id])[0]
        info = track.get_specific_download_info(codec="mp3", bitrate_in_kbps=320)
        if info:
            return info.get_direct_link()
        else:
            logging.info(
                "Couldn't obtain 320kbps download link for track %s",
                self.yandex_track_id,
            )
            return track.get_download_info()[0].get_direct_link()

    # def get_available_quality(self) -> List[int]:
    #     track = client.tracks([self.yandex_track_id])[0]
    #     return [ info.bitrate_in_kbps for info in track.get_download_info()]


def search(query) -> List[YandexTrack]:
    r = client.search(query, type_="track")
    if not r.tracks:
        return None

    return [YandexTrack(track) for track in r.tracks.results[0:20]]


def get_link(track_id: int | str):
    if type(track_id) == str and track_id.find(":") > -1:
        track_id, album_id = track_id.split(":")
        return f"https://music.yandex.ru/album/{album_id}/track/{track_id}"
    else:
        return f"https://music.yandex.ru/track/{track_id}"


def get_track_data(track_id: str | int) -> YandexTrack:
    return YandexTrack.from_id(track_id)
