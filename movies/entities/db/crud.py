from typing import List

from sqlalchemy.orm import Session

from movies.entities.db.models.movie import Movie


def get_movie_by_external_id(s: Session, external_id: int) -> Movie:
    return s.query(Movie).filter(Movie.external_id == external_id).first()


def get_popular_movies(s: Session, limit: int = 10) -> List[Movie]:
    return s.query(Movie).order_by(Movie.popularity.desc()).limit(limit).all()
