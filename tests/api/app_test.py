import pytest
from httpx import AsyncClient
from pytest_mock import MockFixture
from sqlalchemy.engine import Engine

from movies.api import app


@pytest.mark.asyncio
async def test_resolve_movie(db_engine: Engine, mocker: MockFixture):
    query = """
    {
      movies {
        movie(id: 21) {
          popularity
          productionCompanies {
            name
            parentCompany {
              name
            }
          }
        }
      }
    }"""
    # Replace the db_engine used by the app with the test db_engine.
    mocker.patch.object(app, "db_engine", db_engine)
    async with AsyncClient(app=app.app, base_url="http://test") as client:
        response = await client.post("/graphql", json={"query": query})

    assert response.status_code == 200
    data = response.json()["data"]
    assert data is not None
    assert data["movies"]["movie"]["popularity"] == 21.662
