from typing import Optional

from pydantic import BaseModel


class Genre(BaseModel):
    id: int
    external_id: Optional[int]
    name: str
