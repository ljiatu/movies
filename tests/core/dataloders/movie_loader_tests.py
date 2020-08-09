from dataclasses import dataclass
from typing import Any, Dict, List

import pytest
from aresponses import ResponsesMockServer
from pytest_mock import MockFixture
from sqlalchemy.orm import Session
from starlette.datastructures import State

from movies.core.dataloaders.movie_loader import MovieLoader, URL_PATH
from movies.core.db.models.movie import Movie
from movies.core.entities.movie import Movie as EntityMovie
from movies.settings import TMDB_API_HOST, TMDB_API_VERSION


@dataclass
class FakeRequest:
    state: State


@pytest.fixture
def context(db_session: Session) -> Dict[str, Any]:
    state = State({"db_session": db_session})
    return {"request": FakeRequest(state=state)}


@pytest.fixture
def db_movies() -> List[Movie]:
    return [Movie(external_id=1), Movie(external_id=2), Movie(external_id=3)]


@pytest.fixture
def json_movies() -> List[Dict[str, Any]]:
    return [
        {
            "id": 1,
            "adult": False,
            "popularity": 100.09,
            "genres": [],
            "release_date": "2019-09-05",
            "revenue": 1000_000_000,
            "status": "ACTIVE",
            "title": "Aloha",
            "video": False,
            "vote_average": 100.09,
            "vote_count": 3_879_113_121,
        },
        {
            "id": 2,
            "adult": False,
            "popularity": 200.09,
            "genres": [{"id": 1, "name": "Action"}],
            "release_date": "2020-01-31",
            "revenue": 1_000_000,
            "status": "ALIVE",
            "title": "Bonjour",
            "video": True,
            "vote_average": 200.09,
            "vote_count": 198_143_009,
        },
        {
            "id": 3,
            "adult": False,
            "popularity": 300.09,
            "genres": [{"id": 2, "name": "Fantasy"}, {"id": 3, "name": "Thriller"}],
            "release_date": "2020-03-15",
            "revenue": 4000_000_000,
            "status": "RUNNING",
            "title": "Nihao",
            "video": True,
            "vote_average": 138.09,
            "vote_count": 40_879_113_121,
        },
    ]


@pytest.fixture
def movie_keys(db_movies: List[Movie]) -> List[int]:
    return list(map(lambda m: m.external_id, db_movies))


@pytest.fixture
def query_paths(movie_keys: List[int]) -> List[str]:
    return [f"/{TMDB_API_VERSION}/{URL_PATH}/{k}" for k in movie_keys]


@pytest.mark.asyncio
async def test_batch_get_success(
    aresponses: ResponsesMockServer,
    context: Dict[str, Any],
    query_paths: List[str],
    db_movies: List[Movie],
    json_movies: List[Dict[str, Any]],
    movie_keys: List[int],
    mocker: MockFixture,
):
    from movies.core.dataloaders import movie_loader

    mocker.patch.object(movie_loader.crud, "get_movies").return_value = db_movies
    for path, json_movie in zip(query_paths, json_movies):
        aresponses.add(TMDB_API_HOST, path, "GET", response=json_movie)

    movie_loader = MovieLoader.for_context(context)
    movies = await movie_loader.load_many(movie_keys)
    assert movies == [EntityMovie(**jm) for jm in json_movies]

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_batch_get_partial_failure(
    aresponses: ResponsesMockServer,
    context: Dict[str, Any],
    query_paths: List[str],
    db_movies: List[Movie],
    json_movies: List[Dict[str, Any]],
    movie_keys: List[int],
    mocker: MockFixture,
):
    from movies.core.dataloaders import movie_loader

    mocker.patch.object(movie_loader.crud, "get_movies").return_value = db_movies
    # The request for movie_id=2 will fail with a 500.
    aresponses.add(TMDB_API_HOST, query_paths[0], "GET", response=json_movies[0])
    aresponses.add(
        TMDB_API_HOST, query_paths[1], "GET", aresponses.Response(status=500)
    )
    aresponses.add(TMDB_API_HOST, query_paths[2], "GET", response=json_movies[2])

    movie_loader = MovieLoader.for_context(context)
    movies = await movie_loader.load_many(movie_keys)
    assert movies == [
        EntityMovie(**json_movies[0]),
        None,
        EntityMovie(**json_movies[2]),
    ]
