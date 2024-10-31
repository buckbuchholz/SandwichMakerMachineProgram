from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from api.models.models import Recipe
from api.schemas import RecipeCreate, RecipeUpdate

def create(db: Session, recipe: RecipeCreate):
    db_recipe = Recipe(sandwich_id=recipe.sandwich_id, resource_id=recipe.resource_id, amount=recipe.amount)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def read_all(db: Session):
    return db.query(Recipe).all()

def read_one(db: Session, recipe_id: int):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe

def update(db: Session, recipe_id: int, recipe: RecipeUpdate):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id)
    update_data = recipe.dict(exclude_unset=True)
    db_recipe.update(update_data, synchronize_session=False)
    db.commit()
    return db_recipe.first()

def delete(db: Session, recipe_id: int):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id)
    if db_recipe.first() is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db_recipe.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
