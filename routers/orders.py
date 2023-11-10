"""Orders router"""
from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from db import get_db
from controllers.order_controller import OrderController
import schemas

router = APIRouter()


@router.get("/orders", tags=["Orders"], response_model=List[schemas.Order])
def get_orders(db: Session = Depends(get_db)):
    """Get all orders"""
    return OrderController.all(db)


@router.get("/orders/{order_id}", tags=["Orders"], response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get order by order_id"""
    return OrderController.get_by_id(db, order_id)


@router.post("/orders", tags=["Orders"], response_model=schemas.Order)
async def create_order(
    order_request: schemas.OrderCreate, db: Session = Depends(get_db)
):
    """Create order with input data"""
    return await OrderController.create(db, order_request)


@router.delete("/orders/{order_id}", tags=["Orders"])
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete order by order_id"""
    await OrderController.delete(db, order_id)
    return f"Order {order_id} deleted!"


@router.put("/orders/{order_id}", tags=["Orders"], response_model=schemas.Order)
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
