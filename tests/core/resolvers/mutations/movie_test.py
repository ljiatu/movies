from typing import Any, Dict

import pytest
from aresponses import ResponsesMockServer
from fastapi import HTTPException

from movies.core.resolvers.mutations.movie import (
    RatingOutOfBoundException,
    resolve_rate,
)
from movies.settings import TMDB_API_HOST, TMDB_API_VERSION

MOVIE_ID = 1
URL_PATH = f"/{TMDB_API_VERSION}/movie/{MOVIE_ID}/rating"


@pytest.fixture
def ok_response() -> Dict[str, Any]:
    return {"status_code": 1, "status_message": "Success."}


@pytest.mark.asyncio
async def test_resolve_rate(
    aresponses: ResponsesMockServer, ok_response: Dict[str, Any]
):
    aresponses.add(TMDB_API_HOST, URL_PATH, "POST", response=ok_response)
    result = await resolve_rate(movie_id=MOVIE_ID, rating=1.0)
    assert result is True

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_resolve_rate_rating_out_of_bound():
    with pytest.raises(RatingOutOfBoundException):
        await resolve_rate(movie_id=MOVIE_ID, rating=0.1)


@pytest.mark.asyncio
async def test_resolve_rate_tmdb_exception(aresponses: ResponsesMockServer):
    aresponses.add(TMDB_API_HOST, URL_PATH, "POST", aresponses.Response(status=500))

    with pytest.raises(HTTPException):
        await resolve_rate(movie_id=MOVIE_ID, rating=10.0)

    aresponses.assert_plan_strictly_followed()
