from sqlalchemy.orm import Session
from models.worker import Worker

from schemas import WorkerBase, WorkerCreate

class WorkerController:
    
    @staticmethod
    def all(db: Session):
        return db.query(Worker).order_by(Worker.id).all()
    
    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(Worker).get(id)
    
    @staticmethod
    async def create(db: Session, worker: WorkerCreate):
        db_worker = Worker(full_name=worker.full_name, post=worker.post)
        db.add(db_worker)
        db.commit()
        db.refresh(db_worker)
        return db_worker
    
    @staticmethod
    async def delete(db: Session, id: int):
        db.delete(db.query(Worker).get(id))
        db.commit()
    
    @staticmethod
    async def update(db: Session, worker_data):
        updated_worker = db.merge(worker_data)
        db.commit()
        return updated_worker