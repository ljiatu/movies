import asyncio
from typing import Iterable

import aiohttp

from movies.core.clients.tmdb import get
from movies.core.constants import API_KEY, BASE_URL
from movies.core.dataloaders.base import AriadneDataLoader
from movies.core.db import crud
from movies.core.entities.movie import Movie

URL_PATH = "movie"


class MovieLoader(AriadneDataLoader):
    context_key = "movies"

    async def batch_load_fn(self, keys: Iterable[int]) -> Iterable[Movie]:
        s = self.context["request"].state.db_session
        assert s is not None
        db_movies = crud.get_movies(s, keys)
        query_urls = [f"{BASE_URL}/{URL_PATH}/{m.external_id}" for m in db_movies]
        async with aiohttp.ClientSession() as httpSession:
            params = {"api_key": API_KEY}
            movies = await asyncio.gather(
                *(get(httpSession, url, params) for url in query_urls)
            )
            return (Movie(**m) for m in movies)
