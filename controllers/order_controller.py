from sqlalchemy.orm import Session
from models.order import Order

from schemas import OrderBase, OrderCreate


class OrderController:
    @staticmethod
    def all(db: Session):
        return db.query(Order).order_by(Order.id).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(Order).get(id)

    @staticmethod
    async def create(db: Session, order: OrderCreate):
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
    async def delete(db: Session, id: int):
        db.delete(db.query(Order).get(id))
        db.commit()

    @staticmethod
    async def update(db: Session, order_data):
        updated_order = db.merge(order_data)
        db.commit()
        return updated_order
