"""Module of Worker controller"""
from sqlalchemy.orm import Session
from models.worker import Worker

from schemas import WorkerCreate


class WorkerController:
    """Worker controller"""

    @staticmethod
    def all(db: Session):
        """Get all workers"""
        return db.query(Worker).order_by(Worker.id).all()

    @staticmethod
    def get_by_id(db: Session, id_: int):
        """Get worker by id"""
        return db.query(Worker).get(id_)

    @staticmethod
    def get_by_name(db: Session, name: str):
        """Get worker by name"""
        return db.query(Worker).filter(Worker.full_name == name).first()

    @staticmethod
    async def create(db: Session, worker: WorkerCreate):
        """Create Worker"""
        db_worker = Worker(full_name=worker.full_name, post=worker.post)
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
