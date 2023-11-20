"""Module of Order model"""
import datetime

from sqlalchemy import Integer, ForeignKey, Index, DateTime, String, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column    

from db import Base


class Order(Base):
    """Order model"""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text)
    start_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    deadline_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    real_end_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    complexity_level: Mapped[int] = mapped_column(Integer)
    project_id = mapped_column(ForeignKey("projects.cipher"))
    worker_id = mapped_column(ForeignKey("workers.id"))
