"""
Dish management API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Dish
from schemas import DishCreate, DishUpdate, DishResponse

router = APIRouter(prefix="/api/dishes", tags=["dishes"])


@router.get("", response_model=List[DishResponse])
def get_dishes(
    category: str = None,
    available_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Get all dishes, optionally filtered by category and availability.
    Returns dishes grouped by category (client-side grouping).
    """
    query = db.query(Dish)
    
    if available_only:
        query = query.filter(Dish.is_available == True)
    
    if category:
        query = query.filter(Dish.category == category)
    
    dishes = query.all()
    return dishes


@router.post("", response_model=DishResponse, status_code=status.HTTP_201_CREATED)
def create_dish(
    dish: DishCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new dish (Admin only - authentication can be added later).
    """
    db_dish = Dish(**dish.dict())
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


@router.put("/{dish_id}", response_model=DishResponse)
def update_dish(
    dish_id: int,
    dish_update: DishUpdate,
    db: Session = Depends(get_db)
):
    """
    Update dish information (Admin only).
    """
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    
    if not db_dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dish with id {dish_id} not found"
        )
    
    # Update only provided fields
    update_data = dish_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_dish, field, value)
    
    db.commit()
    db.refresh(db_dish)
    return db_dish


@router.get("/{dish_id}", response_model=DishResponse)
def get_dish(
    dish_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single dish by ID.
    """
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dish with id {dish_id} not found"
        )
    
    return dish


