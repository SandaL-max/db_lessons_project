"""Orders router"""
from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from db import get_db
from services.order_service import OrderService
import schemas

router = APIRouter()


@router.get("/orders", tags=["Orders"], response_model=List[schemas.Order])
async def get_orders(
    per_page: int = 10,
    page: int = 0,
    order_by: str = "id",
    db: Session = Depends(get_db),
):
    """Get all orders"""
    orders = await OrderService.all(db, per_page, page, order_by)
    if orders and len(orders) > 0:
        return orders
    else:
        raise HTTPException(status_code=400, detail="Orders are empty or don't exist")


@router.get("/orders/{order_id}", tags=["Orders"], response_model=schemas.Order)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get order by order_id"""
    order = await OrderService.get_by_id(db, order_id)
    if order:
        return order
    else:
        raise HTTPException(
            status_code=400, detail="Order not found with the given order_id"
        )


@router.post("/orders", tags=["Orders"], response_model=schemas.Order)
async def create_order(
    order_request: schemas.OrderCreate, db: Session = Depends(get_db)
):
    """Create order with input data"""
    worker = await OrderService.create(db, order_request)
    if worker:
        return worker
    else:
        raise HTTPException(status_code=400, detail="Can't create order")


@router.delete("/orders/{order_id}", tags=["Orders"])
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete order by order_id"""
    await OrderService.delete(db, order_id)
    return f"Order {order_id} deleted!"


@router.put("/orders/{order_id}", tags=["Orders"], response_model=schemas.Order)
async def update_order(
    order_id: int, order_request: schemas.OrderCreate, db: Session = Depends(get_db)
):
    """Update order with input data"""
    db_order = OrderService.get_by_id(db, order_id)
    if db_order:
        update_order_encoded = jsonable_encoder(order_request)
        db_order.name = update_order_encoded["name"]
        db_order.description = update_order_encoded["description"]
        db_order.start_date = update_order_encoded["start_date"]
        db_order.deadline_date = update_order_encoded["deadline_date"]
        db_order.real_end_date = update_order_encoded["real_end_date"]
        db_order.complexity_level = update_order_encoded["complexity_level"]
        db_order.project_id = update_order_encoded["project_id"]
        db_order.worker_id = update_order_encoded["worker_id"]
        return await OrderService.update(db, db_order)
    else:
        raise HTTPException(
            status_code=400, detail="Item not found with the given order_id"
        )
