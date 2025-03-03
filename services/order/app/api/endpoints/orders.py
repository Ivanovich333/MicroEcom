from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdateStatus
from app.crud import order as order_crud
from app.celery_worker.tasks import process_order
from app.models.state_machine import OrderStateMachine

router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    try:
        db_order = order_crud.create_order(db, order_data)
        
        process_order.delay(str(db_order.id))
        
        return db_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[OrderResponse])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = order_crud.get_orders(db, skip=skip, limit=limit)
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def read_order(order_id: str, db: Session = Depends(get_db)):
    db_order = order_crud.get_order_by_id(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return db_order


@router.get("/user/{user_id}", response_model=List[OrderResponse])
def read_user_orders(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = order_crud.get_user_orders(db, user_id=user_id, skip=skip, limit=limit)
    return orders


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: str, status_update: OrderUpdateStatus, db: Session = Depends(get_db)):
    try:
        db_order = order_crud.update_order_status(db, order_id=order_id, status_update=status_update)
        if db_order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return db_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(order_id: str, db: Session = Depends(get_db)):
    db_order = order_crud.get_order_by_id(db, order_id)
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if not OrderStateMachine.can_cancel(db_order.status):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order cannot be cancelled in its current state ({db_order.status})"
        )
    
    db_order = order_crud.cancel_order(db, order_id=order_id)
    return db_order 