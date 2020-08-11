import asyncio
from typing import Iterable

import aiohttp

from movies.core.clients.tmdb import get
from movies.core.dataloaders.base import AriadneDataLoader
from movies.core.db import crud
from movies.core.entities.movie import Movie
from movies.settings import TMDB_BASE_URL

URL_PATH = "movie"


class MovieLoader(AriadneDataLoader):
    context_key = "movies"

    async def batch_load_fn(self, keys: Iterable[int]) -> Iterable[Movie]:
        s = self.context["request"].state.db_session
        assert s is not None
        db_movies = crud.get_movies(s, keys)
        query_urls = [f"{TMDB_BASE_URL}/{URL_PATH}/{m.external_id}" for m in db_movies]
        async with aiohttp.ClientSession() as httpSession:
            movies = await asyncio.gather(
                *(get(httpSession, url) for url in query_urls), return_exceptions=True,
            )
            return (
                Movie(**m) if not isinstance(m, Exception) else None for m in movies
            )
