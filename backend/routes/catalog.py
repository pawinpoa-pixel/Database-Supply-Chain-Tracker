from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from routes.auth import get_current_user

categories_router = APIRouter(prefix="/categories", tags=["categories"])
products_router = APIRouter(prefix="/products", tags=["products"])


def _get_owned_category_or_404(db: Session, category_id: int, user_id: int) -> models.Category:
    category = (
        db.query(models.Category)
        .filter(models.Category.id == category_id, models.Category.user_id == user_id)
        .first()
    )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def _validate_parent_category(db: Session, parent_category_id: int, user_id: int) -> None:
    parent = _get_owned_category_or_404(db, parent_category_id, user_id)
    return parent


def _get_owned_product_or_404(db: Session, product_id: int, user_id: int) -> models.Product:
    product = (
        db.query(models.Product)
        .filter(models.Product.id == product_id, models.Product.user_id == user_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def _validate_product_refs(db: Session, body: schemas.ProductCreate, user_id: int) -> None:
    if body.category_id is not None:
        _get_owned_category_or_404(db, body.category_id, user_id)
    if body.primary_supplier_id is not None:
        supplier = (
            db.query(models.Supplier)
            .filter(models.Supplier.id == body.primary_supplier_id, models.Supplier.user_id == user_id)
            .first()
        )
        if not supplier:
            raise HTTPException(status_code=404, detail="Primary supplier not found")


@categories_router.get("", response_model=list[schemas.CategoryRead])
def list_categories(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return (
        db.query(models.Category)
        .filter(models.Category.user_id == current_user.id)
        .order_by(models.Category.id)
        .all()
    )


@categories_router.post("", response_model=schemas.CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    body: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if body.parent_category_id is not None:
        _validate_parent_category(db, body.parent_category_id, current_user.id)
    category = models.Category(**body.model_dump(), user_id=current_user.id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@categories_router.put("/{category_id}", response_model=schemas.CategoryRead)
def update_category(
    category_id: int,
    body: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    category = _get_owned_category_or_404(db, category_id, current_user.id)
    if body.parent_category_id is not None:
        _validate_parent_category(db, body.parent_category_id, current_user.id)
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
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    category = _get_owned_category_or_404(db, category_id, current_user.id)
    db.delete(category)
    db.commit()


@products_router.get("", response_model=list[schemas.ProductRead])
def list_products(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return (
        db.query(models.Product)
        .filter(models.Product.user_id == current_user.id)
        .order_by(models.Product.id)
        .all()
    )


@products_router.post("", response_model=schemas.ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    body: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if (
        db.query(models.Product)
        .filter(models.Product.sku == body.sku, models.Product.user_id == current_user.id)
        .first()
    ):
        raise HTTPException(status_code=400, detail="SKU already exists")
    if (
        body.barcode
        and db.query(models.Product)
        .filter(models.Product.barcode == body.barcode, models.Product.user_id == current_user.id)
        .first()
    ):
        raise HTTPException(status_code=400, detail="Barcode already exists")
    _validate_product_refs(db, body, current_user.id)
    product = models.Product(**body.model_dump(), user_id=current_user.id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@products_router.put("/{product_id}", response_model=schemas.ProductRead)
def update_product(
    product_id: int,
    body: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    product = _get_owned_product_or_404(db, product_id, current_user.id)
    existing = (
        db.query(models.Product)
        .filter(
            models.Product.sku == body.sku,
            models.Product.user_id == current_user.id,
            models.Product.id != product_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="SKU already exists")
    if body.barcode:
        barcode_clash = (
            db.query(models.Product)
            .filter(
                models.Product.barcode == body.barcode,
                models.Product.user_id == current_user.id,
                models.Product.id != product_id,
            )
            .first()
        )
        if barcode_clash:
            raise HTTPException(status_code=400, detail="Barcode already exists")
    _validate_product_refs(db, body, current_user.id)
    for key, value in body.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


@products_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    product = _get_owned_product_or_404(db, product_id, current_user.id)
    db.delete(product)
    db.commit()
