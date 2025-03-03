from typing import List, Optional
from sqlalchemy.orm import Session
import requests
import logging
from fastapi import HTTPException, status

from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.schemas.order import OrderCreate, OrderUpdateStatus
from app.core.config import settings
from app.models.state_machine import OrderStateMachine
from app.db.transaction import transaction
from app.utils.redis_lock import lock_manager

logger = logging.getLogger(__name__)


def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
    return db.query(Order).offset(skip).limit(limit).all()


def get_order_by_id(db: Session, order_id: str) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()


def get_user_orders(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Order]:
    return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()


def create_order(db: Session, order: OrderCreate) -> Order:
    total_amount = 0
    order_items = []
    
    for item in order.items:
        try:
            response = requests.get(f"{settings.PRODUCT_SERVICE_URL}/api/v1/products/{item.product_id}")
            response.raise_for_status()
            product_data = response.json()
            
            unit_price = product_data["price"]
            total_price = unit_price * item.quantity
            total_amount += total_price
            
            order_items.append({
                "product_id": item.product_id,
                "product_name": product_data["name"],
                "quantity": item.quantity,
                "unit_price": unit_price,
                "total_price": total_price,
                "stock": product_data["stock"]
            })
            
        except (requests.RequestException, KeyError) as e:
            raise ValueError(f"Error fetching product data: {str(e)}")
    
    for item_data in order_items:
        try:
            with lock_manager.lock(f"product_stock:{item_data['product_id']}", timeout=5):
                response = requests.get(
                    f"{settings.PRODUCT_SERVICE_URL}/api/v1/products/{item_data['product_id']}"
                )
                response.raise_for_status()
                current_stock = response.json()["stock"]
                
                if current_stock < item_data["quantity"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Insufficient stock for product {item_data['product_id']}"
                    )
                
                update_response = requests.patch(
                    f"{settings.PRODUCT_SERVICE_URL}/api/v1/products/{item_data['product_id']}/stock",
                    json={"stock": current_stock - item_data["quantity"]}
                )
                update_response.raise_for_status()
                
        except TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not verify stock for product {item_data['product_id']}"
            )
        except requests.RequestException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Error updating stock for product {item_data['product_id']}: {str(e)}"
            )
    
    with transaction(db) as session:
        db_order = Order(
            user_id=order.user_id,
            status=OrderStatus.PENDING,
            total_amount=total_amount,
            shipping_address=order.shipping_address,
            billing_address=order.billing_address,
            notes=order.notes
        )
        session.add(db_order)
        session.flush()
        
        for item_data in order_items:
            db_item = OrderItem(
                order_id=db_order.id,
                product_id=item_data["product_id"],
                product_name=item_data["product_name"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                total_price=item_data["total_price"]
            )
            session.add(db_item)
        
        session.refresh(db_order)
        return db_order


def update_order_status(db: Session, order_id: str, status_update: OrderUpdateStatus) -> Optional[Order]:
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return None
        
    with transaction(db) as session:
        try:
            OrderStateMachine.validate_transition(db_order.status, status_update.status)
            
            db_order.status = status_update.status
            session.refresh(db_order)
            logger.info(f"Order {order_id} status updated from {db_order.status} to {status_update.status}")
            return db_order
        except ValueError as e:
            logger.error(f"Invalid status transition for order {order_id}: {str(e)}")
            raise ValueError(f"Invalid state transition from {db_order.status} to {status_update.status}")


def cancel_order(db: Session, order_id: str) -> Optional[Order]:
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return None
        
    with transaction(db) as session:
        if OrderStateMachine.can_cancel(db_order.status):
            db_order.status = OrderStatus.CANCELLED
            session.refresh(db_order)
            logger.info(f"Order {order_id} has been cancelled")
            return db_order
        
        logger.warning(f"Cannot cancel order {order_id} in its current state ({db_order.status})")
        return db_order 