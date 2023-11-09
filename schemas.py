"""Store schemas for all models"""
import datetime

from pydantic import BaseModel


class WorkerBase(BaseModel):
    """Base of worker"""

    full_name: str
    post: str


class WorkerCreate(WorkerBase):
    """Schema for creating"""


class Worker(WorkerBase):
    """Schema of worker model"""

    id: int

    class Config:
        """Necessary configuration class"""

        from_attributes = True


class ProjectBase(BaseModel):
    """Base of project"""

    name: str
    end_date: datetime.date
    complexity_level: int


class ProjectCreate(ProjectBase):
    """Schema for creating"""


class Project(ProjectBase):
    """Schema of project model"""

    cipher: int

    class Config:
        """Necessary configuration class"""

        from_attributes = True


class OrderBase(BaseModel):
    """Base of order"""

    start_date: datetime.date
    deadline_date: datetime.date
    real_end_date: datetime.date
    complexity_level: int
    project_id: int
    worker_id: int


class OrderCreate(OrderBase):
    """Schema for creating"""


class Order(OrderBase):
    """Schema of order model"""

    id: int

    class Config:
        """Necessary configuration class"""

        from_attributes = True
