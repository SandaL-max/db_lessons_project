import datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from db import Base

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    deadline_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    real_end_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    complexity_level: Mapped[int] = mapped_column(Integer)
    project_id = mapped_column(ForeignKey("projects.cipher"))
    worker_id = mapped_column(ForeignKey("workers.id"))