from typing import Any, Dict

from aiohttp import ClientResponseError, ClientSession
from fastapi import HTTPException


async def get(
    session: ClientSession, query_url: str, params: Dict[str, str]
) -> Dict[str, Any]:
    async with session.get(query_url, params=params) as resp:
        try:
            resp.raise_for_status()
            return await resp.json()
        except ClientResponseError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Request to TMDB API failed. Status code: {resp.status}. Error: {e}",
            )
