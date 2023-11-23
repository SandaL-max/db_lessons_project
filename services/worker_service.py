"""Module of Worker controller"""
from typing import List, Any
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.worker import Worker

from schemas import WorkerCreate


class WorkerService:
    """Worker Service"""

    @staticmethod
    async def all(db: Session, per_page: int, page: int, order_by: str) -> List[Worker]:
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
    async def get_by_id(db: Session, id_: int) -> Any | None:
        """Get worker by id"""
        return db.query(Worker).get(id_)

    @staticmethod
    async def get_by_name(db: Session, name: str) -> Worker | None:
        """Get worker by name"""
        return db.query(Worker).filter(Worker.full_name == name).first()

    @staticmethod
    async def create(db: Session, worker: WorkerCreate) -> Worker:
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
    async def delete(db: Session, id_: int) -> None:
        """Delete Worker"""
        db.delete(db.query(Worker).get(id_))
        db.commit()

    @staticmethod
    async def update(db: Session, worker_data):
        """Update Worker"""
        updated_worker = db.merge(worker_data)
        db.commit()
        return updated_worker

    @staticmethod
    async def search(db: Session, pattern: str) -> List[Worker]:
        """Search worker with trigramm method"""
        # pylint: disable-next=E1102
        columns = func.coalesce(Worker.full_name, "").concat(
            # pylint: disable-next=E1102
            func.coalesce(Worker.post, "")
        )
        columns = columns.self_group()
        data = (
            db.query(Worker)
            .where(columns.bool_op("%")(pattern))
            .order_by(func.similarity(columns, pattern).desc())
            .all()
        )
        return data

    @staticmethod
    async def regex_by_details(
        db: Session,
        key_name: str,
        pattern: str,
        per_page: int,
        page: int,
    ) -> List[Worker] | None:
        """Get worker by given details column data"""
        if key_name == "":
            return None
        else:
            return (
                db.query(Worker)
                .filter(Worker.details[key_name].astext.match(pattern))
                .order_by(Worker.details[key_name].astext)
                .slice(page * per_page, page * per_page + per_page)
                .all()
            )
