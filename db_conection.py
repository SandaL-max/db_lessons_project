import os
import datetime
from sqlalchemy import Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column
from dotenv import load_dotenv

load_dotenv()
DB = os.getenv("DB")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(
    f"{DB}+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}", echo=False
)
engine.connect()


class Base(DeclarativeBase):
    pass


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    deadline_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    real_end_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    complexity_level: Mapped[int] = mapped_column(Integer)
    project_id = mapped_column(ForeignKey("projects.cipher"))
    worker_id = mapped_column(ForeignKey("workers.id"))


class Project(Base):
    __tablename__ = "projects"

    cipher: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    end_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    complexity_level: Mapped[int] = mapped_column(Integer)


class Worker(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50))
    post: Mapped[str] = mapped_column(String(50))


Base.metadata.create_all(engine)

with Session(engine) as session:
    q = session.query(Worker).filter(Worker.id > 0).all()
    title = f"{'ID':<5} | {'Full name':<20} | {'Post':<20}"
    print(title)
    print("-" * len(title))
    for worker in q:
        print(f"{worker.id:<5} | {worker.full_name:<20} | {worker.post:<10}")
    print("-" * len(title))
    print()

    q = session.query(Project).filter(Project.cipher > 0).all()
    title = (
        f"{'Cipher':<6} | {'Name':<20} | {'End date':<10} | {'Complexity level':<10}"
    )
    print(title)
    print("-" * len(title))
    for project in q:
        print(
            f"{project.cipher:<6} | {project.name:<20} | {project.end_date.strftime('%d.%m.%Y'):<10} | {project.complexity_level:<20}"
        )
    print("-" * len(title))
    print()

    q = session.query(Order).filter(Order.id > 0).all()
    title = f"{'ID':<5} | {'Start date':<10} | {'Deadline date':<10} | {'Real end date':<10} | {'Complexity level':<5} | {'Project ID':<5} | {'Worker ID':<5}"
    print(title)
    print("-" * len(title))
    for order in q:
        print(
            f"{order.id:<5} | "
            + f"{order.start_date.strftime('%d.%m.%Y'):<10} | "
            + f"{order.deadline_date.strftime('%d.%m.%Y'):<13} | "
            + f"{order.real_end_date.strftime('%d.%m.%Y'):<13} | "
            + f"{order.complexity_level:<16} | "
            + f"{order.project_id:<10} | "
            + f"{order.worker_id:<10}"
        )
    print("-" * len(title))
