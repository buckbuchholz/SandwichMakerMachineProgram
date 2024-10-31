from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from api.models.models import OrderDetail
from api.schemas import OrderDetailCreate, OrderDetailUpdate

def create(db: Session, order_detail: OrderDetailCreate):
    db_order_detail = OrderDetail(order_id=order_detail.order_id, sandwich_id=order_detail.sandwich_id, amount=order_detail.amount)
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

def read_all(db: Session):
    return db.query(OrderDetail).all()

def read_one(db: Session, order_detail_id: int):
    db_order_detail = db.query(OrderDetail).filter(OrderDetail.id == order_detail_id).first()
    if db_order_detail is None:
        raise HTTPException(status_code=404, detail="Order Detail not found")
    return db_order_detail

def update(db: Session, order_detail_id: int, order_detail: OrderDetailUpdate):
    db_order_detail = db.query(OrderDetail).filter(OrderDetail.id == order_detail_id)
    update_data = order_detail.dict(exclude_unset=True)
    db_order_detail.update(update_data, synchronize_session=False)
    db.commit()
    return db_order_detail.first()

def delete(db: Session, order_detail_id: int):
    db_order_detail = db.query(OrderDetail).filter(OrderDetail.id == order_detail_id)
    if db_order_detail.first() is None:
        raise HTTPException(status_code=404, detail="Order Detail not found")
    db_order_detail.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

