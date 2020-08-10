import datetime
from typing import List

import pytest
import vcr
from httpx import AsyncClient
from pytest_mock import MockFixture
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from movies.api import app
from movies.core.db.models.movie import Movie


@pytest.fixture
def db_movies() -> List[Movie]:
    return [
        Movie(
            external_id=300671,
            title="13 Hours: The Secret Soldiers of Benghazi",
            release_date=datetime.date(2016, 7, 13),
        ),
        Movie(
            external_id=583083,
            title="The Kissing Booth 2",
            release_date=datetime.date(2020, 7, 24),
        ),
        Movie(
            external_id=547016,
            title="The Old Guard",
            release_date=datetime.date(2020, 7, 10),
        ),
    ]


@pytest.mark.asyncio
@vcr.use_cassette(
    "tests/fixtures/vcr_cassettes/movies.yaml",
    ignore_hosts=[
        "test"
    ],  # Ignore the `test` host because we are testing sending real requests to the app.
)
async def test_resolve_movie(
    db_engine: Engine,
    db_movies: List[Movie],
    unsafe_db_session: Session,
    mocker: MockFixture,
):
    query = """
    {
      movies {
        movie(id: 1) {
          popularity
          adult
          productionCompanies {
            name
            parentCompany {
              name
            }
          }
        }
      }
    }"""
    # Populate the DB with movies
    unsafe_db_session.add_all(db_movies)
    unsafe_db_session.commit()

    # Replace the db_engine used by the app with the test db_engine.
    mocker.patch.object(app, "db_engine", db_engine)
    async with AsyncClient(app=app.app, base_url="http://test") as client:
        response = await client.post("/graphql", json={"query": query})

    assert response.status_code == 200
    data = response.json()["data"]
    assert data is not None
    assert data["movies"]["movie"]["popularity"] == 18.009
    assert not data["movies"]["movie"]["adult"]
    assert data["movies"]["movie"]["productionCompanies"][0]["name"] == "Paramount"
