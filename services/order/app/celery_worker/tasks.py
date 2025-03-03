import time
import requests
import logging
from sqlalchemy.orm import Session
from celery import shared_task
from fastapi import HTTPException, status

from app.celery_worker.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.order import OrderStatus
from app.crud.order import get_order_by_id, update_order_status
from app.schemas.order import OrderUpdateStatus
from app.core.config import settings
from app.models.state_machine import OrderStateMachine
from app.db.transaction import transaction
from app.utils.redis_lock import lock_manager

logger = logging.getLogger(__name__)

def restore_product_stock(product_id: str, quantity: int) -> None:
    try:
        with lock_manager.lock(f"product_stock:{product_id}", timeout=5):
            response = requests.get(
                f"{settings.PRODUCT_SERVICE_URL}/api/v1/products/{product_id}"
            )
            response.raise_for_status()
            current_stock = response.json()["stock"]
            
            update_response = requests.patch(
                f"{settings.PRODUCT_SERVICE_URL}/api/v1/products/{product_id}/stock",
                json={"stock": current_stock + quantity}
            )
            update_response.raise_for_status()
            logger.info(f"Restored {quantity} units of stock for product {product_id}")
    except Exception as e:
        logger.error(f"Failed to restore stock for product {product_id}: {str(e)}")

@celery_app.task(name="process_order")
def process_order(order_id: str) -> str:
    logger.info(f"Processing order {order_id}")
    
    db = SessionLocal()
    
    try:
        order = get_order_by_id(db, order_id)
        if not order:
            logger.error(f"Order {order_id} not found")
            return f"Error: Order {order_id} not found"
        
        if order.status != OrderStatus.PENDING:
            logger.info(f"Order {order_id} is in {order.status} state, skipping processing")
            return f"Order {order_id} is in {order.status} state, processing skipped"
        
        try:
            with transaction(db) as session:
                update_order_status(session, order_id, OrderUpdateStatus(status=OrderStatus.PROCESSING))
                logger.info(f"Updated order {order_id} status to PROCESSING")
        except ValueError as e:
            logger.error(f"Failed to update order status: {str(e)}")
            return f"Error: Failed to update order status: {str(e)}"
        
        for item in order.items:
            try:
                response = requests.get(
                    f"{settings.PRODUCT_SERVICE_URL}/api/v1/products/{item.product_id}"
                )
                response.raise_for_status()
                product_data = response.json()
                
                if product_data["stock"] < item.quantity:
                    logger.error(f"Insufficient stock for product {item.product_id}")
                    with transaction(db) as session:
                        update_order_status(session, order_id, OrderUpdateStatus(status=OrderStatus.CANCELLED))
                    return f"Error: Insufficient stock for product {item.product_id}"
                
                logger.info(f"Product {item.product_id} is available")
                
            except requests.RequestException as e:
                logger.error(f"Error verifying product {item.product_id}: {str(e)}")
                for processed_item in order.items[:order.items.index(item)]:
                    restore_product_stock(processed_item.product_id, processed_item.quantity)
                return f"Error verifying product: {str(e)}"
        
        try:
            login_data = {
                "username": settings.USER_SERVICE_ADMIN_EMAIL,
                "password": settings.USER_SERVICE_ADMIN_PASSWORD
            }
            auth_response = requests.post(
                f"{settings.USER_SERVICE_URL}/api/v1/login/access-token", 
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            auth_response.raise_for_status()
            token = auth_response.json()["access_token"]
                
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{settings.USER_SERVICE_URL}/api/v1/users/{order.user_id}", 
                headers=headers
            )
            response.raise_for_status()
            logger.info(f"User {order.user_id} verified successfully")
        except requests.RequestException as e:
            logger.error(f"Error verifying user {order.user_id}: {str(e)}")
            for item in order.items:
                restore_product_stock(item.product_id, item.quantity)
            return f"Error verifying user: {str(e)}"
        
        order = get_order_by_id(db, order_id)
        if order.status != OrderStatus.PROCESSING:
            logger.info(f"Order {order_id} is no longer in PROCESSING state (current: {order.status}), not updating to SHIPPED")
            for item in order.items:
                restore_product_stock(item.product_id, item.quantity)
            return f"Order {order_id} is in {order.status} state, not updating to SHIPPED"
        
        try:
            with transaction(db) as session:
                update_order_status(session, order_id, OrderUpdateStatus(status=OrderStatus.SHIPPED))
                logger.info(f"Updated order {order_id} status to SHIPPED")
                return f"Order {order_id} processed successfully"
        except ValueError as e:
            logger.error(f"Failed to update order status to SHIPPED: {str(e)}")
            for item in order.items:
                restore_product_stock(item.product_id, item.quantity)
            return f"Error: Failed to update order status to SHIPPED: {str(e)}"
            
    except Exception as e:
        logger.exception(f"Error processing order {order_id}: {str(e)}")
        for item in order.items:
            restore_product_stock(item.product_id, item.quantity)
        return f"Error: {str(e)}"
    
    finally:
        db.close() 