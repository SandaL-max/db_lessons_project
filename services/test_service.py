"""Module of Test Controller"""
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from models.order import Order
from models.worker import Worker

from data_generator import generate_workers, generate_projects, generate_orders


class TestService:
    """Test Service"""

    @staticmethod
    async def get_join_of_workers_and_orders(
        db: Session, per_page: int, page: int
    ) -> list:
        """Get join of workers and orders"""
        data = (
            db.query(Worker)
            .join(Order)
            .filter(Worker.id == Order.worker_id)
            .order_by(Worker.id)
            .slice(page * per_page, page * per_page + per_page)
            .all()
        )
        result = []
        for worker in data:
            result.append(
                {
                    "id": worker.id,
                    "full_name": worker.full_name,
                    "post": worker.post,
                    "salary": worker.salary,
                    "orders": worker.orders,
                }
            )
        return result

    @staticmethod
    async def get_orders_count_for_workers(
        db: Session, per_page: int, page: int
    ) -> list:
        """Get orders count for workers"""
        data = (
            # pylint: disable-next=E1102
            db.query(Worker, func.count(Worker.orders).label("order_count"))
            .join(Order)
            .group_by(Worker.id)
            .slice(page * per_page, page * per_page + per_page)
        )
        result = []
        for worker in data:
            result.append(
                {
                    "id": worker[0].id,
                    "full_name": worker[0].full_name,
                    "post": worker[0].post,
                    "salary": worker[0].salary,
                    "orders_count": worker[1],
                }
            )
        return result

    @staticmethod
    async def get_workers_with_complexity_level(
        db: Session, complexity_level: int, per_page: int, page: int
    ) -> list:
        """Get workers with given comlexity level or bigger than that"""
        subquery = (
            db.query(Order.worker_id)
            .filter(Order.complexity_level >= complexity_level)
            .subquery()
        )
        query = (
            db.query(Worker)
            .filter(Worker.id.in_(select(subquery)))
            .slice(page * per_page, page * per_page + per_page)
        )
        result = []
        for worker in query:
            result.append(
                {
                    "id": worker.id,
                    "full_name": worker.full_name,
                    "post": worker.post,
                    "salary": worker.salary,
                }
            )
        return result

    @staticmethod
    async def update_post(db: Session, new_post: str) -> None:
        """Update post of workers, whose real end date is less than deadline date"""
        subquery = (
            db.query(Order.worker_id)
            .filter(Order.real_end_date <= Order.deadline_date)
            .subquery()
        )
        db.query(Worker).filter(Worker.id.in_(select(subquery))).update(
            {"post": new_post}
        )
        db.commit()

    @staticmethod
    async def generate_workers_by_quantity(db: Session, quantity: int) -> str:
        """Generate some workers"""
        data = await generate_workers(quantity)
        db.add_all(data)
        db.commit()
        return "Create workers was successful"

    @staticmethod
    async def generate_projects_by_quantity(db: Session, quantity: int) -> str:
        """Generate some projects"""
        data = await generate_projects(quantity)
        db.add_all(data)
        db.commit()
        return "Create projects was successful"

    @staticmethod
    async def generate_orders_by_quantity(
        db: Session,
        quantity: int,
        project_id_range: tuple,
        worker_id_range: tuple,
    ) -> str:
        """Generate some workers"""
        data = await generate_orders(quantity, project_id_range, worker_id_range)
        db.add_all(data)
        db.commit()
        return "Create orders was successful"

    @staticmethod
    async def get_salary_median(db: Session) -> int:
        """Get median of workers salary"""
        data = db.query(func.round(func.avg(Worker.salary))).scalar()
        return data
