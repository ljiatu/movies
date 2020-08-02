from datetime import datetime

from pydantic import BaseModel


class Movie(BaseModel):
    popularity: float
    vote_count: int
    video: bool
    poster_path: str
    external_id: int
    adult: bool
    backdrop_path: str
    original_language: str
    original_title: str
    title: str
    vote_average: float
    overview: str
    release_date: datetime.date
