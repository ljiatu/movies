from datetime import date
from typing import List

from pydantic import BaseModel

from movies.entities.genre import Genre


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
    release_date: date
    genres: List[Genre]

    class Config:
        orm_mode = True
