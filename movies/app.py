from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from movies.entities import movie
from movies.entities.db import crud
from movies.entities.db.session import SessionLocal

app = FastAPI()


def get_session():
    s = SessionLocal()
    try:
        yield s
    finally:
        s.close()


@app.get("/movies/popular", response_model=List[movie.Movie])
async def get_popular_movies(limit: int = 10, s: Session = Depends(get_session)):
    return crud.get_popular_movies(s, limit)
