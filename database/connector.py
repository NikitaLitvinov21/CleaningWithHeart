from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import get_config
from models.base import Base
from models.booking import Booking  # noqa
from models.customer import Customer  # noqa
from models.user import User  # noqa

database_config = get_config("database")

USERNAME = database_config["user"]
PASSWORD = database_config["password"]
HOST = database_config["host"]
PORT = database_config["port"]
DATABASE_NAME = database_config["name"]

if not USERNAME or not PASSWORD or not HOST or not PORT or not DATABASE_NAME:
    raise RuntimeError("Cannot obtain database setting!")

DATABASE_URL = (
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
)

engine: Engine = create_engine(DATABASE_URL, echo=database_config["echo"])

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
