import datetime

from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from db import Base

class Project(Base):
    __tablename__ = "projects"

    cipher: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    end_date: Mapped[datetime.date] = mapped_column(Date)
    complexity_level: Mapped[int] = mapped_column(Integer)