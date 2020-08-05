from movies.core.db.models.base_class import Base
from sqlalchemy import Column, Integer, String


class Genre(Base):
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, index=True, nullable=False)
    name = Column(String, nullable=False)
