from typing import Dict, Optional

from pydantic import BaseModel, model_validator


class SongInfoExtractEvent(BaseModel):
    cifra_club_url: Optional[str] = None
    song_raw_sheet: Optional[Dict] = None
    download_and_analyse_song: Optional[bool] = False

    @model_validator(mode="before")
    def any_of(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field is required.")
        return values


class Context(BaseModel):
    aws_request_id: Optional[str] = None
