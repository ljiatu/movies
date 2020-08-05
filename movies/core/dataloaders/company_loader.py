from typing import List

from movies.core.clients.tmdb import get
from movies.core.constants import API_KEY, BASE_URL
from movies.core.dataloaders.base import AriadneDataLoader
from movies.core.entities.company import Company

URL_PATH = "company"


class CompanyLoader(AriadneDataLoader):
    context_key = "companies"

    async def batch_load_fn(self, keys: List[int]):
        query_urls = [f"{BASE_URL}/{URL_PATH}/{k}?api_key={API_KEY}" for k in keys]
        return [Company(**get(url)) for url in query_urls]
