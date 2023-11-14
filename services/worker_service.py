"""Module of Worker controller"""
from sqlalchemy.orm import Session
from models.worker import Worker

from schemas import WorkerCreate


class WorkerService:
    """Worker Service"""

    @staticmethod
    async def all(db: Session, per_page: int, page: int, order_by: str):
        """Get all workers"""
        if order_by == "id":
            order_obj = Worker.id
        elif order_by == "name":
            order_obj = Worker.full_name
        elif order_by == "salary":
            order_obj = Worker.salary
        else:
            order_obj = Worker.id
        return (
            db.query(Worker)
            .order_by(order_obj)
            .slice(page * per_page, page * per_page + per_page)
            .all()
        )

    @staticmethod
    async def get_by_id(db: Session, id_: int):
        """Get worker by id"""
        return db.query(Worker).get(id_)

    @staticmethod
    async def get_by_name(db: Session, name: str):
        """Get worker by name"""
        return db.query(Worker).filter(Worker.full_name == name).first()

    @staticmethod
    async def create(db: Session, worker: WorkerCreate):
        """Create Worker"""
        db_worker = Worker(
            full_name=worker.full_name,
            post=worker.post,
            salary=worker.salary,
        )
        db.add(db_worker)
        db.commit()
        db.refresh(db_worker)
        return db_worker

    @staticmethod
    async def delete(db: Session, id_: int):
        """Delete Worker"""
        db.delete(db.query(Worker).get(id_))
        db.commit()

    @staticmethod
    async def update(db: Session, worker_data):
        """Update Worker"""
        updated_worker = db.merge(worker_data)
        db.commit()
        return updated_worker
