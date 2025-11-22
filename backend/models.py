"""
SQLAlchemy database models
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Dish(Base):
    """
    Dish model - represents a menu item
    """
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)  # e.g., "Meat", "Veggie", "Soup", "Dessert"
    image_url = Column(String, nullable=True)
    tags = Column(String, nullable=True)  # Comma-separated tags like "Spicy,Sweet"
    rating = Column(Integer, default=3)  # 1-5 rating
    is_available = Column(Boolean, default=True, index=True)

    # Relationship to order_items
    order_items = relationship("OrderItem", back_populates="dish")


class Order(Base):
    """
    Order model - represents a customer order
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_time = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String, default="pending", index=True)  # "pending", "accepted", "cooking", "completed"
    note = Column(Text, nullable=True)  # User remarks
    total_items = Column(Integer, default=0)

    # Relationship to order_items
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    """
    OrderItem model - association table for orders and dishes
    """
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    dish_id = Column(Integer, ForeignKey("dishes.id"), nullable=True)  # Nullable in case dish is deleted
    dish_name = Column(String, nullable=False)  # Snapshot of dish name
    quantity = Column(Integer, default=1, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
    dish = relationship("Dish", back_populates="order_items")


