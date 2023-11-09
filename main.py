"""Programm entry point"""
from typing import List

import socket
from sqlalchemy.orm import Session
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from db import get_db, engine, Base
from controllers.worker_controller import WorkerController
from controllers.order_controller import OrderController
from controllers.projects_controller import ProjectController
import schemas

app = FastAPI()

Base.metadata.create_all(bind=engine)


# Workers
@app.get("/workers", tags=["Workers"], response_model=List[schemas.Worker])
def get_workers(db: Session = Depends(get_db)):
    """Get all workers"""
    return WorkerController.all(db)


@app.get("/workers/{worker_id}", tags=["Workers"], response_model=schemas.Worker)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    """Get worker by worker_id"""
    return WorkerController.get_by_id(db, worker_id)


@app.post("/workers", tags=["Workers"], response_model=schemas.Worker)
async def create_worker(
    worker_request: schemas.WorkerCreate, db: Session = Depends(get_db)
):
    """Create worker with input data"""
    return await WorkerController.create(db, worker_request)


@app.delete("/workers/{worker_id}", tags=["Workers"])
async def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    """Delete worker by worker_id"""
    await WorkerController.delete(db, worker_id)
    return f"Worker {worker_id} deleted!"


@app.put("/workers/{worker_id}", tags=["Workers"], response_model=schemas.Worker)
async def update_worker(
    worker_id: int, worker_request: schemas.WorkerCreate, db: Session = Depends(get_db)
):
    """Update worker with input data"""
    db_worker = WorkerController.get_by_id(db, worker_id)
    if db_worker:
        update_worker_encoded = jsonable_encoder(worker_request)
        db_worker.full_name = update_worker_encoded["full_name"]
        db_worker.post = update_worker_encoded["post"]
        return await WorkerController.update(db, db_worker)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given id_")


# Projects
@app.get("/projects", tags=["Projects"], response_model=List[schemas.Project])
def get_projects(db: Session = Depends(get_db)):
    """Get all projects"""
    return ProjectController.all(db)


@app.get("/projects/{project_id}", tags=["Projects"], response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get project by project_id"""
    return ProjectController.get_by_id(db, project_id)


@app.post("/projects", tags=["Projects"], response_model=schemas.Project)
async def create_project(
    project_request: schemas.ProjectCreate, db: Session = Depends(get_db)
):
    """Create project with input data"""
    return await ProjectController.create(db, project_request)


@app.delete("/projects/{project_id}", tags=["Projects"])
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete project by project_id"""
    await ProjectController.delete(db, project_id)
    return f"Project {project_id} deleted!"


@app.put("/projects/{project_id}", tags=["Projects"], response_model=schemas.Project)
async def update_project(
    project_id: int,
    project_request: schemas.ProjectCreate,
    db: Session = Depends(get_db),
):
    """Update project with input data"""
    db_project = ProjectController.get_by_id(db, project_id)
    if db_project:
        update_project_encoded = jsonable_encoder(project_request)
        db_project.name = update_project_encoded["name"]
        db_project.end_date = update_project_encoded["end_date"]
        db_project.complexity_level = update_project_encoded["complexity_level"]
        return await ProjectController.update(db, db_project)
    else:
        raise HTTPException(
            status_code=400, detail="Item not found with the given project_id"
        )


# Orders
@app.get("/orders", tags=["Orders"], response_model=List[schemas.Order])
def get_orders(db: Session = Depends(get_db)):
    """Get all orders"""
    return OrderController.all(db)


@app.get("/orders/{order_id}", tags=["Orders"], response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get order by order_id"""
    return OrderController.get_by_id(db, order_id)


@app.post("/orders", tags=["Orders"], response_model=schemas.Order)
async def create_order(
    order_request: schemas.OrderCreate, db: Session = Depends(get_db)
):
    """Create order with input data"""
    return await OrderController.create(db, order_request)


@app.delete("/orders/{order_id}", tags=["Orders"])
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete order by order_id"""
    await OrderController.delete(db, order_id)
    return f"Order {order_id} deleted!"


@app.put("/orders/{order_id}", tags=["Orders"], response_model=schemas.Order)
async def update_order(
    order_id: int, order_request: schemas.OrderCreate, db: Session = Depends(get_db)
):
    """Update order with input data"""
    db_order = OrderController.get_by_id(db, order_id)
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
        raise HTTPException(
            status_code=400, detail="Item not found with the given order_id"
        )


if __name__ == "__main__":
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    uvicorn.run(
        app="main:app", host=ip_address, port=8000, log_level="info", reload=True
    )
