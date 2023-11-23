"""Module of Worker model"""
from typing import List, Any

from sqlalchemy import Integer, String, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db import Base


class Worker(Base):
    """Worker model"""

    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    post: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[dict[str, Any]] = mapped_column(
        JSONB(none_as_null=True), nullable=False
    )
    salary: Mapped[int] = mapped_column(Integer, nullable=False)

    orders: Mapped[List["Order"]] = relationship()

    index = Index(
        "workers_details_idx",
        details,
        unique=False,
        postgresql_using="gin",
        postgresql_ops={
            "json_details": "jsonb_path_ops",
        },
    )
