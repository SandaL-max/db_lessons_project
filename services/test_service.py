"""Module of Test Controller"""
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from models.order import Order
from models.worker import Worker
from models.project import Project

from schemas import OrderCreate, WorkerCreate, ProjectCreate


class TestService:
    """Test Service"""

    @staticmethod
    async def get_join_of_workers_and_orders(db: Session):
        """Get join of workers and orders"""
        data = (
            db.query(Worker)
            .join(Order)
            .filter(Worker.id == Order.worker_id)
            .order_by(Worker.id)
            .all()
        )
        result = []
        for worker in data:
            result.append(
                {
                    "id": worker.id,
                    "full_name": worker.full_name,
                    "post": worker.post,
                    "orders": worker.orders,
                }
            )
        return result

    @staticmethod
    async def get_orders_count_for_workers(db: Session):
        """Get orders count for workers"""
        data = (
            db.query(Worker, func.count(Worker.orders).label("order_count"))
            .join(Order)
            .group_by(Worker.id)
        )
        print(data)
        result = []
        for worker in data:
            result.append(
                {
                    "id": worker[0].id,
                    "full_name": worker[0].full_name,
                    "post": worker[0].post,
                    "orders_count": worker[1],
                }
            )
        return result

    @staticmethod
    async def get_workers_with_complexity_level(db: Session, complexity_level: int):
        """Get workers with given comlexity level or bigger than that"""
        subquery = (
            db.query(Order.worker_id)
            .filter(Order.complexity_level >= complexity_level)
            .subquery()
        )
        query = db.query(Worker).filter(Worker.id.in_(select(subquery)))
        result = []
        for worker in query:
            result.append(
                {
                    "id": worker.id,
                    "full_name": worker.full_name,
                    "post": worker.post,
                }
            )
        return result

    @staticmethod
    async def update_post(db: Session, new_post: str):
        """Update post of workers, whose real end date is less than deadline date"""
        subquery = (
            db.query(Order.worker_id)
            .filter(Order.real_end_date <= Order.deadline_date)
            .subquery()
        )
        query = (
            db.query(Worker)
            .filter(Worker.id.in_(select(subquery)))
            .update({"post": new_post})
        )
        db.commit()
