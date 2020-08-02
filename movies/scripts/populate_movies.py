import json
from typing import Any, Dict

from sqlalchemy.orm import Session

from movies.entities.db.genre import Genre
from movies.entities.db.movie import Movie
from movies.entities.db.session import SessionLocal


def populate_movies(s: Session):
    with open("./movies.json") as f:
        movies = json.load(f)
        all_genres = s.query(Genre).all()
        genres_by_external_id = {g.external_id: g for g in all_genres}
        movie_objs = [_parse_movie(m, genres_by_external_id) for m in movies]
        s.add_all(movie_objs)
        s.commit()


def _parse_movie(movie: Dict[str, Any], genres_by_external_id: Dict[int, Genre]) -> Movie:
    movie_obj = Movie(**{k: v for k, v in movie.items() if k not in ["id", "genre_ids"]})
    movie_obj.external_id = movie["id"]
    movie_obj.genres = [genres_by_external_id[gid] for gid in movie["genre_ids"]]
    return movie_obj


if __name__ == "__main__":
    s = SessionLocal()
    populate_movies(s)
