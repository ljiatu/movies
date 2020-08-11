import asyncio
from typing import Iterable

import aiohttp

from movies.core.clients.tmdb import get
from movies.core.dataloaders.base import AriadneDataLoader
from movies.core.entities.company import Company
from movies.settings import TMDB_BASE_URL

URL_PATH = "company"


class CompanyLoader(AriadneDataLoader):
    context_key = "companies"

    async def batch_load_fn(self, keys: Iterable[int]) -> Iterable[Company]:
        query_urls = [f"{TMDB_BASE_URL}/{URL_PATH}/{k}" for k in keys]
        async with aiohttp.ClientSession() as httpSession:
            companies = await asyncio.gather(
                *(get(httpSession, url) for url in query_urls), return_exceptions=True,
            )
            return (
                Company(**c) if not isinstance(c, Exception) else None
                for c in companies
            )
