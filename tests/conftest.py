import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from tests.settings import TEST_DB_URL

engine = create_engine(TEST_DB_URL)
SessionLocal = scoped_session(sessionmaker(bind=engine))


@pytest.fixture
def db_session():
    return SessionLocal()
