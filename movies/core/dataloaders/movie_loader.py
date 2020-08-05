from typing import List

from movies.core.clients.tmdb import get
from movies.core.constants import API_KEY, BASE_URL
from movies.core.dataloaders.base import AriadneDataLoader
from movies.core.db import crud
from movies.core.entities.movie import Movie

URL_PATH = "movie"


class MovieLoader(AriadneDataLoader):
    context_key = "movies"

    async def batch_load_fn(self, keys: List[int]):
        s = self.context["request"].state.db_session
        assert s is not None
        db_movies = crud.get_movies(s, keys)
        query_urls = [
            f"{BASE_URL}/{URL_PATH}/{m.external_id}?api_key={API_KEY}"
            for m in db_movies
        ]
        return [Movie(**get(url)) for url in query_urls]
