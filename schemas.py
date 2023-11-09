import datetime
from typing import List, Optional

from pydantic import BaseModel

class WorkerBase(BaseModel):
    full_name: str
    post: str

class WorkerCreate(WorkerBase):
    pass

class Worker(WorkerBase):
    id: int
    
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str
    end_date: datetime.date
    complexity_level: int

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    cipher: int
    
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    id: int
    start_date: datetime.date
    deadline_date: datetime.date
    real_end_date: datetime.date
    complexity_level: int
    project_id: int
    worker_id: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    
    class Config:
        orm_mode = True