from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from routes.auth import get_current_user

categories_router = APIRouter(prefix="/categories", tags=["categories"])
products_router = APIRouter(prefix="/products", tags=["products"])


@categories_router.get("", response_model=list[schemas.CategoryRead])
def list_categories(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(models.Category).order_by(models.Category.id).all()


@categories_router.post("", response_model=schemas.CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(body: schemas.CategoryCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    category = models.Category(**body.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@categories_router.put("/{category_id}", response_model=schemas.CategoryRead)
def update_category(
    category_id: int,
    body: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    category = db.get(models.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if body.parent_category_id is not None:
        visited = set()
        current_id = body.parent_category_id
        while current_id is not None:
            if current_id == category_id:
                raise HTTPException(status_code=400, detail="Circular category hierarchy is not allowed")
            if current_id in visited:
                break
            visited.add(current_id)
            parent_row = db.get(models.Category, current_id)
            current_id = parent_row.parent_category_id if parent_row else None
    for key, value in body.model_dump().items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


@categories_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    category = db.get(models.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()


@products_router.get("", response_model=list[schemas.ProductRead])
def list_products(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(models.Product).order_by(models.Product.id).all()


@products_router.post("", response_model=schemas.ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(body: schemas.ProductCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if db.query(models.Product).filter(models.Product.sku == body.sku).first():
        raise HTTPException(status_code=400, detail="SKU already exists")
    if body.barcode and db.query(models.Product).filter(models.Product.barcode == body.barcode).first():
        raise HTTPException(status_code=400, detail="Barcode already exists")
    product = models.Product(**body.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@products_router.put("/{product_id}", response_model=schemas.ProductRead)
def update_product(
    product_id: int,
    body: schemas.ProductCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    existing = db.query(models.Product).filter(models.Product.sku == body.sku, models.Product.id != product_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")
    if body.barcode:
        barcode_clash = (
            db.query(models.Product)
            .filter(models.Product.barcode == body.barcode, models.Product.id != product_id)
            .first()
        )
        if barcode_clash:
            raise HTTPException(status_code=400, detail="Barcode already exists")
    for key, value in body.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@products_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
