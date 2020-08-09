from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from movies.settings import DB_URL

engine = create_engine(DB_URL)
SessionLocal = scoped_session(sessionmaker(bind=engine))
