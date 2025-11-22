"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Dish Schemas
class DishBase(BaseModel):
    name: str
    category: str
    image_url: Optional[str] = None
    tags: Optional[str] = None
    rating: int = Field(ge=1, le=5, default=3)
    is_available: bool = True


class DishCreate(DishBase):
    pass


class DishUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    is_available: Optional[bool] = None


class DishResponse(DishBase):
    id: int

    class Config:
        from_attributes = True


# OrderItem Schemas
class OrderItemBase(BaseModel):
    dish_id: int
    quantity: int = Field(ge=1, default=1)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    dish_id: Optional[int]
    dish_name: str
    quantity: int

    class Config:
        from_attributes = True


# Order Schemas
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    note: Optional[str] = None


class OrderResponse(BaseModel):
    id: int
    order_time: datetime
    status: str
    note: Optional[str]
    total_items: int
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|accepted|cooking|completed)$")


