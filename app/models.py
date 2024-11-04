from datetime import date

from pydantic import BaseModel, ValidationError, computed_field
from pydantic.v1 import root_validator


class MusicInfoExtractEvent(BaseModel):
    cifra_club_url: str | None = None
    song_raw_sheet: dict | None = None
    download_and_analyse_song: bool | None = False

    @root_validator
    def any_of(cls, v):
        if not any(v.values()):
            raise ValueError(f'At least one field are required: "({v.values()})"')




class Context(BaseModel):
    aws_request_id: str | None = None
