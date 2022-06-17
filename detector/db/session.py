from contextlib import contextmanager
from typing import Generator

from sqlalchemy.orm import Session as SQLAlchmeySession
from sqlalchemy.orm import scoped_session, sessionmaker

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False))


@contextmanager
def session_scope() -> Generator[SQLAlchmeySession, None, None]:  # pragma: no cover
    """Provide a transactional scope around a series of operations."""
    session: SQLAlchmeySession = Session()
    try:
        yield session
        session.commit()
    except BaseException as e:
        session.rollback()
        raise e
    finally:
        session.close()
