"""Module of Order Controller"""
from sqlalchemy.orm import Session
from models.order import Order

from schemas import OrderCreate


class OrderService:
    """Order Service"""

    @staticmethod
    def all(db: Session):
        """Get all orders"""
        return db.query(Order).order_by(Order.id).all()

    @staticmethod
    def get_by_id(db: Session, id_: int):
        """Get order by id"""
        return db.query(Order).get(id_)

    @staticmethod
    async def create(db: Session, order: OrderCreate):
        """Create order"""
        db_order = Order(
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
    async def delete(db: Session, id_: int):
        """Delete order"""
        db.delete(db.query(Order).get(id_))
        db.commit()

    @staticmethod
    async def update(db: Session, order_data):
        """Update order"""
        updated_order = db.merge(order_data)
        db.commit()
        return updated_order
