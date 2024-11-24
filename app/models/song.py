from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, Dict, List


class GenreIcons(SQLModel, table=False):
    light: str
    lightInactive: str
    dark: str
    darkInactive: str


class Image(SQLModel, table=False):
    hashPath: str
    thumbnail_50: str = Field(alias="50")
    thumbnail_162: str = Field(alias="162")
    thumbnail_250: str = Field(alias="250")
    color: str


class HeadImage(SQLModel, table=False):
    color: str


class InappropriateContent(SQLModel, table=False):
    artist: bool
    albuns: bool
    photos: bool


from sqlmodel import SQLModel, Field, create_engine, Session, select, Column, JSON
from typing import Optional, Dict


class Genre(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    url: str
    icons: Dict[str, str] = Field(sa_column=Column(JSON))  # JSON column for icons


class Artist(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    url: str
    totalPhotos: int
    genre_id: Optional[int] = Field(foreign_key="genre.id")
    image: Dict[str, str] = Field(sa_column=Column(JSON))  # JSON column for image data
    headImage: Dict[str, str] = Field(
        sa_column=Column(JSON)
    )  # JSON column for headImage data
    inappropriateContent: Dict[str, bool] = Field(
        sa_column=Column(JSON)
    )  # JSON column for inappropriate content
    songs: List["Song"] = Field(sa_column=Column(JSON))  # This can remain nullable
    externalURLs: Dict[str, Optional[str]] = Field(
        sa_column=Column(JSON)
    )  # JSON column for external URLs


class Song(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    url: str
    artist_id: int = Field(foreign_key="artist.id")
    hits: int
    verified: bool
    mod: str
    videoLessonId: Optional[int]
    reviewed: int
    ranking_position: int


DATABASE_URL = "sqlite:///songs.db"
engine = create_engine(DATABASE_URL)

# Create all tables
SQLModel.metadata.create_all(engine)

from typing import List


def save_songs_to_db(songs_data: List[dict], session: Session):
    for position, song_data in enumerate(
        songs_data, start=1
    ):  # start from 1 for ranking
        artist_data = song_data.pop("artist")

        # Parse Artist and Genre
        genre_data = artist_data.pop("genre")
        genre = Genre(**genre_data)

        # Add Genre if it doesn't exist
        existing_genre = session.exec(select(Genre).where(Genre.id == genre.id)).first()
        if not existing_genre:
            session.add(genre)

        artist = Artist(**artist_data)
        artist.genre_id = genre.id

        # Add Artist if it doesn't exist
        existing_artist = session.exec(
            select(Artist).where(Artist.id == artist.id)
        ).first()
        if not existing_artist:
            session.add(artist)

        # Parse and add Song with ranking position
        song = Song(**song_data, ranking_position=position)  # Assign ranking position
        song.artist_id = artist.id
        session.add(song)

    # Commit all changes to the database
    session.commit()
