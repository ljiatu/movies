from sqlalchemy import Column, Integer, String

from movies.entities.db.base_class import Base


class Genre(Base):
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, index=True, nullable=False)
    name = Column(String, nullable=False)
