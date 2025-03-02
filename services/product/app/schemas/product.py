from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0, default=0)
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[float] = Field(gt=0, default=None)


class ProductInDBBase(ProductBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Product(ProductInDBBase):
    pass


class ProductInDB(ProductInDBBase):
    pass 