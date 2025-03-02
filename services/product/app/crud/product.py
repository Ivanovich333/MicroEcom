from typing import List, Optional, Dict, Any, Union

from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get(db: Session, product_id: str) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()


def get_by_name(db: Session, name: str) -> Optional[Product]:
    return db.query(Product).filter(Product.name == name).first()


def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()


def create(db: Session, *, obj_in: ProductCreate) -> Product:
    db_obj = Product(
        name=obj_in.name,
        description=obj_in.description,
        price=obj_in.price,
        stock=obj_in.stock,
        image_url=obj_in.image_url,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, *, db_obj: Product, obj_in: Union[ProductUpdate, Dict[str, Any]]
) -> Product:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)
    
    for field in update_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, *, product_id: str) -> Product:
    obj = db.query(Product).get(product_id)
    db.delete(obj)
    db.commit()
    return obj 