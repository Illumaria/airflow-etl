from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .constants import POSTGRES_DB_URI

engine = create_engine(POSTGRES_DB_URI, client_encoding="utf8")
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope() -> Session:  # type: ignore
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
