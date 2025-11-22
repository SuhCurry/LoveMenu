"""
Order management API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models import Order, OrderItem, Dish
from schemas import OrderCreate, OrderResponse, OrderStatusUpdate

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new order with items.
    """
    # Validate that all dishes exist and are available
    dish_ids = [item.dish_id for item in order_data.items]
    dishes = db.query(Dish).filter(Dish.id.in_(dish_ids)).all()
    dish_dict = {dish.id: dish for dish in dishes}
    
    if len(dishes) != len(dish_ids):
        missing_ids = set(dish_ids) - set(dish_dict.keys())
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dishes not found: {missing_ids}"
        )
    
    # Check availability
    unavailable = [dish for dish in dishes if not dish.is_available]
    if unavailable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unavailable dishes: {[d.name for d in unavailable]}"
        )
    
    # Calculate total items
    total_items = sum(item.quantity for item in order_data.items)
    
    # Create order
    order = Order(
        note=order_data.note,
        total_items=total_items,
        status="pending"
    )
    db.add(order)
    db.flush()  # Get order.id
    
    # Create order items
    for item_data in order_data.items:
        dish = dish_dict[item_data.dish_id]
        order_item = OrderItem(
            order_id=order.id,
            dish_id=item_data.dish_id,
            dish_name=dish.name,
            quantity=item_data.quantity
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(order)
    
    # Load items for response
    order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    return order


@router.get("", response_model=List[OrderResponse])
def get_orders(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get order history (recent first).
    """
    orders = db.query(Order).order_by(Order.order_time.desc()).limit(limit).all()
    
    # Load items for each order
    for order in orders:
        order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    return orders


@router.get("/active", response_model=OrderResponse)
def get_active_order(
    db: Session = Depends(get_db)
):
    """
    Get the current active order (status != completed).
    """
    order = db.query(Order).filter(Order.status != "completed").order_by(Order.order_time.desc()).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active order found"
        )
    
    # Load items
    order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    """
    Update order status (Admin only).
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    order.status = status_update.status
    db.commit()
    db.refresh(order)
    
    # Load items
    order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    return order


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single order by ID.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    
    # Load items
    order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    
    return order


