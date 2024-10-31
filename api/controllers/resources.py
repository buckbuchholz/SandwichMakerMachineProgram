from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from api.models.models import Resource
from api.schemas import ResourceCreate, ResourceUpdate

def create(db: Session, resource: ResourceCreate):
    db_resource = Resource(item=resource.item, amount=resource.amount)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def read_all(db: Session):
    return db.query(Resource).all()

def read_one(db: Session, resource_id: int):
    db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

def update(db: Session, resource_id: int, resource: ResourceUpdate):
    db_resource = db.query(Resource).filter(Resource.id == resource_id)
    update_data = resource.dict(exclude_unset=True)
    db_resource.update(update_data, synchronize_session=False)
    db.commit()
    return db_resource.first()

def delete(db: Session, resource_id: int):
    db_resource = db.query(Resource).filter(Resource.id == resource_id)
    if db_resource.first() is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    db_resource.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
