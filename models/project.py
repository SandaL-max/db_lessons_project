"""Module of Project model"""
import datetime
from typing import List

from sqlalchemy import Integer, String, Index, Date, Text, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db import Base


class Project(Base):
    """Project model"""

    __tablename__ = "projects"

    cipher: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    complexity_level: Mapped[int] = mapped_column(Integer)

    orders: Mapped[List["Order"]] = relationship()

    index = Index(
        "projects_name_description_idx",
        # pylint: disable-next=E1102
        func.coalesce(name, "").concat(func.coalesce(description, "")).label("columns"),
        postgresql_using="gin",
        postgresql_ops={
            "columns": "gin_trgm_ops",
        },
    )
