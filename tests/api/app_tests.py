import pytest
from httpx import AsyncClient

from movies.api.app import app


@pytest.mark.asyncio
async def test_resolve_movie():
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
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/graphql", json={"query": query})

    assert response.status_code == 200
    data = response.json()["data"]
    assert data is not None
    assert data["movies"]["movie"]["popularity"] == 21.662
