from typing import Any, Dict

import requests
from fastapi import HTTPException


def get(query_url: str) -> Dict[str, Any]:
    resp = requests.get(query_url)
    if not resp.ok:
        raise HTTPException(
            status_code=500,
            detail=f"Request to TMDB API failed. Status code: {resp.status_code}. Error: {resp.json()}",
        )

    return resp.json()
