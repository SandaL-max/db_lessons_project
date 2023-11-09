from sqlalchemy.orm import Session
from models.order import Order

class OrderController:
    
    @staticmethod
    def all(db: Session):
        orders = db.query(Order).order_by(Order.id).all()
        orders_list = []
        for order in orders:
            orders_list.append(order.to_dict())
        return orders_list
    
    @staticmethod
    def get_by_id(db: Session, id: int):
        order = db.query(Order).get(id)
        if order:
            return order.to_dict()
        else:
            return None