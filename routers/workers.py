"""Workers router"""
from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from db import get_db
from services.worker_service import WorkerService
import schemas

router = APIRouter()


@router.get("/workers", tags=["Workers"], response_model=List[schemas.Worker])
async def get_workers(db: Session = Depends(get_db)):
    """Get all workers"""
    workers = await WorkerService.all(db)
    if workers and len(workers) > 0:
        return workers
    else:
        raise HTTPException(
            status_code=400, detail="Workers are empty or doesn't exist"
        )


@router.get("/workers/worker", tags=["Workers"], response_model=schemas.Worker)
async def get_worker(
    worker_id: int | None = None,
    worker_name: str | None = None,
    db: Session = Depends(get_db),
):
    """Get accurate worker"""
    if worker_id is not None:
        worker = await WorkerService.get_by_id(db, worker_id)
        if worker:
            return worker
        else:
            raise HTTPException(status_code=400, detail="Can't get worker by given id")
    elif worker_name is not None:
        worker = await WorkerService.get_by_name(db, worker_name)
        if worker:
            return worker
        else:
            raise HTTPException(
                status_code=400, detail="Can't get worker by given name"
            )
    else:
        raise HTTPException(status_code=400, detail="Wrong query parametrs")


@router.post("/workers", tags=["Workers"], response_model=schemas.Worker)
async def create_worker(
    worker_request: schemas.WorkerCreate, db: Session = Depends(get_db)
):
    """Create worker with input data"""
    worker = await WorkerService.create(db, worker_request)
    if worker:
        return worker
    else:
        raise HTTPException(status_code=400, detail="Can't create worker")


@router.delete("/workers/{worker_id}", tags=["Workers"])
async def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    """Delete worker by worker_id"""
    await WorkerService.delete(db, worker_id)
    return f"Worker {worker_id} deleted!"


@router.put("/workers/{worker_id}", tags=["Workers"], response_model=schemas.Worker)
async def update_worker(
    worker_id: int, worker_request: schemas.WorkerCreate, db: Session = Depends(get_db)
):
    """Update worker with input data"""
    db_worker = WorkerService.get_by_id(db, worker_id)
    if db_worker:
        update_worker_encoded = jsonable_encoder(worker_request)
        db_worker.full_name = update_worker_encoded["full_name"]
        db_worker.post = update_worker_encoded["post"]
        return await WorkerService.update(db, db_worker)
    else:
        raise HTTPException(
            status_code=400, detail="Worker not found with the given id"
        )
