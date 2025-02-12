import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from models.base import Base
from models.user import User        # noqa
from models.booking import Booking  # noqa

USERNAME = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
DATABASE_NAME = os.getenv("POSTGRES_DB")

if not USERNAME or not PASSWORD or not HOST or not PORT or not DATABASE_NAME:
    raise RuntimeError(
        "Use 'flask run' instead direct run app.py otherwise .env not set!"
    )

DATABASE_URL = (
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
)

engine: Engine = create_engine(DATABASE_URL)

session_factory = sessionmaker(engine, expire_on_commit=False)


def get_session() -> Session:
    """Provide a new session for interacting with the database."""

    with session_factory() as session:
        return session


def create_tables():
    """Create all tables defined by models inheriting from Base."""

    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all tables defined by models inheriting from Base."""

    Base.metadata.drop_all(bind=engine)
