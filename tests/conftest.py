import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.orm.session import SessionTransaction
from sqlalchemy_utils import create_database, database_exists, drop_database

from movies.core.db.models.base_class import Base
from tests.settings import TEST_DB_URL


@pytest.fixture(scope="session")
def db_engine() -> Engine:
    if not database_exists(TEST_DB_URL):
        create_database(TEST_DB_URL)
    engine = create_engine(TEST_DB_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    drop_database(TEST_DB_URL)


@pytest.fixture
def db_session(db_engine: Engine):
    """Function-scoped sqlalchemy database session"""
    connection = db_engine.connect()

    # begin a non-ORM transaction
    trans = connection.begin()

    # bind an individual Session to the connection
    db_session = _create_db_session(connection)

    # start the session in a SAVEPOINT...
    db_session.begin_nested()

    # then each time that SAVEPOINT ends, reopen it
    @event.listens_for(db_session, "after_transaction_end")
    def restart_savepoint(session: Session, transaction: SessionTransaction):
        if (
            transaction.nested and not transaction._parent.nested
        ):  # pylint: disable=W0212

            # ensure that state is expired the way
            # session.commit() at the top level normally does
            # (optional step)
            session.expire_all()
            session.begin_nested()

    yield db_session
    db_session.close()

    # rollback - everything that happened with the
    # Session above (including calls to commit())
    # is rolled back.
    trans.rollback()

    # return connection to the Engine
    connection.close()


@pytest.fixture()
def unsafe_db_session(db_engine: Engine):
    """
        db fixture which does not wrap tests in a transaction meaning data can be persisted between tests
        If you use this fixture - CLEAN UP AFTER YOURSELF!

        This is useful to make fixtures that are visible in other sessions
        If we made fixtures inside a transaction, they would not be visible in other sessions
    """
    db_session = _create_db_session(db_engine)

    yield db_session
    db_session.close()


def _create_db_session(engine: Engine) -> Session:
    db_session = scoped_session(sessionmaker(bind=engine))()
    Base.metadata.bind = engine  # type: ignore
    return db_session
