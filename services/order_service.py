"""Module of Order Controller"""
from typing import List
from sqlalchemy.orm import Session
from models.order import Order

from schemas import OrderCreate


class OrderService:
    """Order Service"""

    @staticmethod
    async def all(db: Session, per_page: int, page: int, order_by: str) -> List[Order]:
        """Get all orders"""
        if order_by == "id":
            order_obj = Order.id
        elif order_by == "name":
            order_obj = Order.name
        elif order_by == "start_date":
            order_obj = Order.start_date
        elif order_by == "complexity_level":
            order_obj = Order.complexity_level
        else:
            order_obj = Order.id
        return (
            db.query(Order)
            .order_by(order_obj)
            .slice(page * per_page, page * per_page + per_page)
            .all()
        )

    @staticmethod
    async def get_by_id(db: Session, id_: int) -> Order | None:
        """Get order by id"""
        return db.query(Order).get(id_)

    @staticmethod
    async def create(db: Session, order: OrderCreate) -> Order:
        """Create order"""
        db_order = Order(
            name=order.name,
            description=order.description,
            start_date=order.start_date,
            deadline_date=order.deadline_date,
            real_end_date=order.real_end_date,
            complexity_level=order.complexity_level,
            project_id=order.project_id,
            worker_id=order.worker_id,
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    @staticmethod
    async def delete(db: Session, id_: int) -> None:
        """Delete order"""
        db.delete(db.query(Order).get(id_))
        db.commit()

    @staticmethod
    async def update(db: Session, order_data) -> Order:
        """Update order"""
        updated_order = db.merge(order_data)
        db.commit()
        return updated_order
