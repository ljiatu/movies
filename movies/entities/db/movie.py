from sqlalchemy import Column, Integer, String, Boolean, Float, Date, Table, ForeignKey
from sqlalchemy.orm import relationship

from movies.entities.db.base_class import Base

movie_genres = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)


class Movie(Base):
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, index=True, nullable=False)
    popularity = Column(Float)
    vote_count = Column(Integer)
    video = Column(Boolean)
    poster_path = Column(String)
    adult = Column(Boolean)
    backdrop_path = Column(String)
    original_language = Column(String)
    original_title = Column(String)
    title = Column(String, nullable=False)
    vote_average = Column(Float)
    overview = Column(String)
    release_date = Column(Date, nullable=False)

    genres = relationship("Genre", secondary=movie_genres)
