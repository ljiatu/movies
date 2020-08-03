from pydantic import BaseModel


class Genre(BaseModel):
    external_id: int
    name: str

    class Config:
        orm_mode = True
