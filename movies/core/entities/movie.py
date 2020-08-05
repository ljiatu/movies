from typing import List, Optional

from movies.core.entities.company import Company
from movies.core.entities.genre import Genre
from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: int
    adult: bool
    backdrop_path: Optional[str]
    budget: Optional[int]
    homepage: Optional[str]
    imdb_id: Optional[str] = Field(
        Optional[str], min_length=9, max_length=9, regex="^tt[0-9]{7}"
    )
    external_id: Optional[int]
    genres: List[Genre]
    original_language: Optional[str]
    original_title: Optional[str]
    overview: Optional[str]
    popularity: float
    poster_path: Optional[str]
    production_companies: Optional[List[Company]]
    release_date: str
    revenue: int
    runtime: Optional[int]
    status: str
    tagline: Optional[str]
    title: str
    video: bool
    vote_average: float
    vote_count: int
