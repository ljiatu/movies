import asyncio
from typing import Iterable

import aiohttp

from movies.core.clients.tmdb import get
from movies.core.constants import API_KEY, BASE_URL
from movies.core.dataloaders.base import AriadneDataLoader
from movies.core.entities.company import Company

URL_PATH = "company"


class CompanyLoader(AriadneDataLoader):
    context_key = "companies"

    async def batch_load_fn(self, keys: Iterable[int]) -> Iterable[Company]:
        query_urls = [f"{BASE_URL}/{URL_PATH}/{k}" for k in keys]
        async with aiohttp.ClientSession() as httpSession:
            params = {"api_key": API_KEY}
            companies = await asyncio.gather(
                *(get(httpSession, url, params) for url in query_urls),
                return_exceptions=True,
            )
            return (
                Company(**c) if not isinstance(c, Exception) else None
                for c in companies
            )
