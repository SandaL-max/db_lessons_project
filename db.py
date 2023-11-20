"""Create connection to db"""
import os
from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
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

    type_annotation_map = {dict[str, Any]: JSONB}


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Return session object for working with db"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
