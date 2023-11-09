from typing import List, Optional

import socket
from sqlalchemy.orm import Session
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from db import get_db, engine, Base
from controllers.worker_controller import WorkerController
from controllers.order_controller import OrderController
from controllers.projects_controller import ProjectController
import schemas as schemas

app = FastAPI()

Base.metadata.create_all(bind=engine)


# Workers
@app.get("/workers", tags=["Workers"], response_model=List[schemas.Worker])
def get_workers(db: Session = Depends(get_db)):
    return WorkerController.all(db)


@app.get("/workers/{id}", tags=["Workers"], response_model=schemas.Worker)
def get_worker(id: int, db: Session = Depends(get_db)):
    return WorkerController.get_by_id(db, id)


@app.post("/workers", tags=["Workers"], response_model=schemas.Worker)
async def create_worker(
    worker_request: schemas.WorkerCreate, db: Session = Depends(get_db)
):
    return await WorkerController.create(db, worker_request)


@app.delete("/workers/{id}", tags=["Workers"])
async def delete_worker(id: int, db: Session = Depends(get_db)):
    await WorkerController.delete(db, id)
    return f"Worker {id} deleted!"


@app.put("/workers/{id}", tags=["Workers"], response_model=schemas.Worker)
async def update_worker(
    id: int, worker_request: schemas.WorkerCreate, db: Session = Depends(get_db)
):
    db_worker = WorkerController.get_by_id(db, id)
    if db_worker:
        update_worker_encoded = jsonable_encoder(worker_request)
        db_worker.full_name = update_worker_encoded["full_name"]
        db_worker.post = update_worker_encoded["post"]
        return await WorkerController.update(db, db_worker)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")


# Projects
@app.get("/projects", tags=["Projects"], response_model=List[schemas.Project])
def get_projects(db: Session = Depends(get_db)):
    return ProjectController.all(db)


@app.get("/projects/{id}", tags=["Projects"], response_model=schemas.Project)
def get_project(id: int, db: Session = Depends(get_db)):
    return ProjectController.get_by_id(db, id)


@app.post("/projects", tags=["Projects"], response_model=schemas.Project)
async def create_project(
    project_request: schemas.ProjectCreate, db: Session = Depends(get_db)
):
    return await ProjectController.create(db, project_request)


@app.delete("/projects/{id}", tags=["Projects"])
async def delete_project(id: int, db: Session = Depends(get_db)):
    await ProjectController.delete(db, id)
    return f"Project {id} deleted!"


@app.put("/projects/{id}", tags=["Projects"], response_model=schemas.Project)
async def update_project(
    id: int, project_request: schemas.ProjectCreate, db: Session = Depends(get_db)
):
    db_project = ProjectController.get_by_id(db, id)
    if db_project:
        update_project_encoded = jsonable_encoder(project_request)
        db_project.name = update_project_encoded["name"]
        db_project.end_date = update_project_encoded["end_date"]
        db_project.complexity_level = update_project_encoded["complexity_level"]
        return await ProjectController.update(db, db_project)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")


# Orders
@app.get("/orders", tags=["Orders"], response_model=List[schemas.Order])
def get_orders(db: Session = Depends(get_db)):
    return OrderController.all(db)


@app.get("/orders/{id}", tags=["Orders"], response_model=schemas.Order)
def get_order(id: int, db: Session = Depends(get_db)):
    return OrderController.get_by_id(db, id)


@app.post("/orders", tags=["Orders"], response_model=schemas.Order)
async def create_order(
    order_request: schemas.OrderCreate, db: Session = Depends(get_db)
):
    return await OrderController.create(db, order_request)


@app.delete("/orders/{id}", tags=["Orders"])
async def delete_order(id: int, db: Session = Depends(get_db)):
    await OrderController.delete(db, id)
    return f"Order {id} deleted!"


@app.put("/orders/{id}", tags=["Orders"], response_model=schemas.Order)
async def update_order(
    id: int, order_request: schemas.OrderCreate, db: Session = Depends(get_db)
):
    db_order = OrderController.get_by_id(db, id)
    if db_order:
        update_order_encoded = jsonable_encoder(order_request)
        db_order.start_date = update_order_encoded["start_date"]
        db_order.deadline_date = update_order_encoded["deadline_date"]
        db_order.real_end_date = update_order_encoded["real_end_date"]
        db_order.complexity_level = update_order_encoded["complexity_level"]
        db_order.project_id = update_order_encoded["project_id"]
        db_order.worker_id = update_order_encoded["worker_id"]
        return await OrderController.update(db, db_order)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")


if __name__ == "__main__":
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    uvicorn.run("main:app", host=ip_address, port=8000, log_level="info", reload=True)
