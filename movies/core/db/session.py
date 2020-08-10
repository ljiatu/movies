from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker

from movies.core.db.models.base_class import Base
from movies.settings import DB_URL

db_engine = create_engine(DB_URL)


def create_db_session(engine: Engine) -> scoped_session:
    Base.metadata.bind = engine  # type: ignore
    return scoped_session(sessionmaker(bind=engine))
