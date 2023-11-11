"""Module of Test Controller"""
from sqlalchemy.orm import Session
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
