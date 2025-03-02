from typing import Any, List, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import product as product_crud
from app.db.session import get_db
from app.schemas.product import Product, ProductCreate, ProductUpdate

router = APIRouter()


@router.get("/health", response_model=Dict[str, str])
def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "product"}


@router.get("/products", response_model=List[Product])
def read_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    products = product_crud.get_multi(db, skip=skip, limit=limit)
    return products


@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    *,
    db: Session = Depends(get_db),
    product_in: ProductCreate,
) -> Any:
    product = product_crud.get_by_name(db, name=product_in.name)
    if product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists",
        )
    product = product_crud.create(db, obj_in=product_in)
    return product


@router.get("/products/{product_id}", response_model=Product)
def read_product(
    *,
    db: Session = Depends(get_db),
    product_id: str,
) -> Any:
    product = product_crud.get(db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.put("/products/{product_id}", response_model=Product)
def update_product(
    *,
    db: Session = Depends(get_db),
    product_id: str,
    product_in: ProductUpdate,
) -> Any:
    product = product_crud.get(db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    product = product_crud.update(db, db_obj=product, obj_in=product_in)
    return product


@router.delete("/products/{product_id}", response_model=Product)
def delete_product(
    *,
    db: Session = Depends(get_db),
    product_id: str,
) -> Any:
    product = product_crud.get(db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    product = product_crud.remove(db, product_id=product_id)
    return product 