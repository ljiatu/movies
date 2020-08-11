from typing import Any, Dict, Optional

from aiohttp import ClientResponseError, ClientSession
from fastapi import HTTPException

from movies.settings import TMDB_API_KEY


async def get(
    session: ClientSession, query_url: str, params: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    if params is None:
        params = {}
    params["api_key"] = TMDB_API_KEY
    async with session.get(query_url, params=params) as resp:
        try:
            resp.raise_for_status()
            return await resp.json()
        except ClientResponseError as e:
            raise HTTPException(
                status_code=500,
                detail=f"GET request to TMDB API failed. Status code: {resp.status}. Error: {e}",
            )


async def post(
    session: ClientSession,
    query_url: str,
    data: Dict,
    params: Optional[Dict[str, str]] = None,
) -> None:
    if params is None:
        params = {}
    params["api_key"] = TMDB_API_KEY
    async with session.post(query_url, data=data, params=params) as resp:
        try:
            resp.raise_for_status()
        except ClientResponseError as e:
            raise HTTPException(
                status_code=500,
                detail=f"POST request to TMDB API failed. Status code: {resp.status}. Error: {e}",
            )
