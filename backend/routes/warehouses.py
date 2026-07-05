from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from routes.auth import get_current_user

warehouses_router = APIRouter(prefix="/warehouses", tags=["warehouses"])
inventory_router = APIRouter(prefix="/inventory", tags=["inventory"])


@warehouses_router.get("", response_model=list[schemas.WarehouseRead])
def list_warehouses(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(models.Warehouse).order_by(models.Warehouse.id).all()


@warehouses_router.post("", response_model=schemas.WarehouseRead, status_code=status.HTTP_201_CREATED)
def create_warehouse(body: schemas.WarehouseCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    warehouse = models.Warehouse(**body.model_dump())
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse


@warehouses_router.put("/{warehouse_id}", response_model=schemas.WarehouseRead)
def update_warehouse(
    warehouse_id: int,
    body: schemas.WarehouseCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    warehouse = db.get(models.Warehouse, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    for key, value in body.model_dump().items():
        setattr(warehouse, key, value)
    db.commit()
    db.refresh(warehouse)
    return warehouse


@warehouses_router.delete("/{warehouse_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    warehouse = db.get(models.Warehouse, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    db.delete(warehouse)
    db.commit()


@inventory_router.get("/low-stock", response_model=list[schemas.InventoryRead])
def low_stock(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return (
        db.query(models.Inventory)
        .join(models.Product, models.Inventory.product_id == models.Product.id)
        .filter(models.Inventory.quantity_on_hand <= models.Product.reorder_level)
        .all()
    )


@inventory_router.get("", response_model=list[schemas.InventoryRead])
def list_inventory(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(models.Inventory).order_by(models.Inventory.id).all()


@inventory_router.post("", response_model=schemas.InventoryRead, status_code=status.HTTP_201_CREATED)
def create_inventory(body: schemas.InventoryCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    existing = (
        db.query(models.Inventory)
        .filter(
            models.Inventory.warehouse_id == body.warehouse_id,
            models.Inventory.product_id == body.product_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Inventory row for this product/warehouse already exists, edit it instead",
        )
    inventory = models.Inventory(**body.model_dump())
    db.add(inventory)
    db.flush()
    if inventory.quantity_on_hand:
        db.add(
            models.InventoryLog(
                inventory_id=inventory.id,
                transaction_type="initial_stock",
                quantity_change=inventory.quantity_on_hand,
                reference_type=None,
                reference_id=None,
                performed_by=None,
            )
        )
    db.commit()
    db.refresh(inventory)
    return inventory


@inventory_router.put("/{inventory_id}", response_model=schemas.InventoryRead)
def update_inventory(
    inventory_id: int,
    body: schemas.InventoryCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    inventory = db.get(models.Inventory, inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory row not found")
    delta = body.quantity_on_hand - inventory.quantity_on_hand
    inventory.warehouse_id = body.warehouse_id
    inventory.product_id = body.product_id
    inventory.quantity_on_hand = body.quantity_on_hand
    if delta:
        db.add(
            models.InventoryLog(
                inventory_id=inventory.id,
                transaction_type="adjustment",
                quantity_change=delta,
                reference_type=None,
                reference_id=None,
                performed_by=None,
            )
        )
    db.commit()
    db.refresh(inventory)
    return inventory


@inventory_router.delete("/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory(inventory_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    inventory = db.get(models.Inventory, inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory row not found")
    db.delete(inventory)
    db.commit()
