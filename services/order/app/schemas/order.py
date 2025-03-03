from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.models.order import OrderStatus


class OrderItemBase(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: str
    product_name: str
    unit_price: float
    total_price: float
    created_at: datetime
    
    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    user_id: str
    shipping_address: str
    billing_address: str
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdateStatus(BaseModel):
    status: OrderStatus


class OrderResponse(OrderBase):
    id: str
    status: OrderStatus
    total_amount: float
    items: List[OrderItemResponse]
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True 