from typing import List, Literal
from urllib.parse import urljoin

import httpx
from sqlmodel import Session

from app.core.logger import get_advanced_logger
from app.models import Song, parse_songs
from app.models.song import engine, save_songs_to_db

log = get_advanced_logger("CifraClubLogger")

CIFRA_CLUB_BASE_API_URL = "https://api.cifraclub.com.br/v3/"
TOP_SONGS_ENDPOINT = "tops"


PERIOD: Literal["semana", "mes", "ano"] = "semana"
GENRE: Literal["blues", "bossa-nova", "gospelreligioso"] = "gospelreligioso"


def get_top_songs_query_params(
    *,
    limit_songs: int = 90,
    limit_artists: int = 45,
    offset_songs: int = 0,
    offset_artists: int = 0,
    period: str = PERIOD,
    genre: str = GENRE,
    instrument: str = "all",
) -> dict:
    return {
        "genre": genre,
        "instrument": instrument,
        "period": period,
        "limitSongs": limit_songs,
        "limitArtists": limit_artists,
        "offsetSongs": offset_songs,
        "offsetArtists": offset_artists,
    }


def get_top_songs_url():
    return urljoin(CIFRA_CLUB_BASE_API_URL, TOP_SONGS_ENDPOINT)


def get_top_songs_url_with_query_params(
    period: str = PERIOD, genre: str = GENRE
) -> str:
    top_songs_url = get_top_songs_url()
    query_params_dict = get_top_songs_query_params(
        limit_songs=90,
        limit_artists=45,
        offset_songs=0,
        offset_artists=0,
        period=period,
        genre=genre,
        instrument="all",
    )

    query_params = "&".join(
        f"{key}={value}" for key, value in query_params_dict.items()
    )

    return f"{top_songs_url}?{query_params}"


def get_top_songs(period: str = PERIOD, genre: str = GENRE) -> List[Song]:
    top_songs_url = get_top_songs_url_with_query_params(period=period, genre=genre)

    log.info(f"Fetching top songs from {top_songs_url}")

    top_songs_response = httpx.get(top_songs_url)

    top_songs_json = top_songs_response.json()

    songs = parse_songs(top_songs_json["songs"])

    with Session(engine) as session:
        save_songs_to_db(top_songs_json["songs"], session)

    return songs
