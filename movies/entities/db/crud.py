from typing import List

from movies.entities.db.models.movie import Movie
from sqlalchemy.orm import Session


def get_movie(s: Session, id: int) -> Movie:
    return s.query(Movie).get(id)


def get_popular_movies(s: Session, limit: int = 10) -> List[Movie]:
    return s.query(Movie).order_by(Movie.popularity.desc()).limit(limit).all()
