from dataclasses import dataclass
import config

from yandex_music import Client

client = Client(config.YAM_TOKEN).init()

@dataclass
class Track:
    title: str
    artists: str
    link: str
    cover_url: str
    duration: int
    download_link: str

def search(query):
    r = client.search(query, type_="track")
    if not r.tracks:
        return None
    
    result = []

    for track in r.tracks.results[0:20]:
        if track.available:
            name = track.title
            id = f"{track.id}:{track.albums[0].id}"
            artists = []
            for artist in track.artists:
                artists.append(artist.name)
            artists = ", ".join(artists)
            result.append({'artist': artists, 'caption': f"{name}", "id": id})
    return result

def get_download_link(track_id):
    track = client.tracks([track_id])
    return track[0].get_download_info()[0].get_direct_link()

def get_link(track_id):
    track_id, album_id = track_id.split(":")
    return f"https://music.yandex.ru/album/{album_id}/track/{track_id}"

def get_track_data(track_id) -> Track:
    track = client.tracks([track_id])[0]
    
    duration = int(track.duration_ms / 1000) if track.duration_ms else 0
    title = track.title
    artists = []
    for artist in track.artists:
        artists.append(artist.name)
    artists = ", ".join(artists)

    download_link = track.get_download_info()[0].get_direct_link()
    
    cover = track.cover_uri.replace("%%", "400x400")
    
    return Track(
        title=title,
        artists=artists,
        link=get_link(track_id),
        download_link=download_link,
        cover_url=f"https://{cover}",
        duration=duration
    )


if __name__ == "__main__":
    print(get_download_link("70562908:11931354"))
