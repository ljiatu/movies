from pydantic import BaseModel


class Genre(BaseModel):
    external_id: int
    name: str
