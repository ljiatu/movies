from typing import List

from sqlalchemy.orm import Session

from movies.core.db.models.movie import Movie


def get_movies(s: Session, ids: List[int]) -> List[Movie]:
    return s.query(Movie).filter(Movie.id.in_(ids)).all()


def get_popular_movies(s: Session, limit: int = 10) -> List[Movie]:
    return s.query(Movie).order_by(Movie.popularity.desc()).limit(limit).all()
