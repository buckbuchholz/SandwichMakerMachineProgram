from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from api.models.models import Order
from api.schemas import OrderCreate, OrderUpdate

def create(db: Session, order: OrderCreate):
    db_order = Order(customer_name=order.customer_name, description=order.description)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def read_all(db: Session):
    return db.query(Order).all()

def read_one(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

def update(db: Session, order_id: int, order: OrderUpdate):
    db_order = db.query(Order).filter(Order.id == order_id)
    update_data = order.dict(exclude_unset=True)
    db_order.update(update_data, synchronize_session=False)
    db.commit()
    return db_order.first()

def delete(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id)
    if db_order.first() is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
