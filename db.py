"""Create connection to db"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv

load_dotenv()
DB_URI = os.getenv("DB_URI")
engine = create_engine(DB_URI, echo=False)
if not database_exists(engine.url):
    create_database(engine.url)
else:
    engine.connect()


class Base(DeclarativeBase):
    """Base model class"""


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Return session object for working with db"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
