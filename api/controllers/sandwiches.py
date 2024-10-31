from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from api.models.models import Sandwich
from api.schemas import SandwichCreate, SandwichUpdate

def create(db: Session, sandwich: SandwichCreate):
    db_sandwich = Sandwich(sandwich_name=sandwich.sandwich_name, price=sandwich.price)
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

def read_all(db: Session):
    return db.query(Sandwich).all()

def read_one(db: Session, sandwich_id: int):
    db_sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if db_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return db_sandwich

def update(db: Session, sandwich_id: int, sandwich: SandwichUpdate):
    db_sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id)
    update_data = sandwich.dict(exclude_unset=True)
    db_sandwich.update(update_data, synchronize_session=False)
    db.commit()
    return db_sandwich.first()

def delete(db: Session, sandwich_id: int):
    db_sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id)
    if db_sandwich.first() is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    db_sandwich.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
