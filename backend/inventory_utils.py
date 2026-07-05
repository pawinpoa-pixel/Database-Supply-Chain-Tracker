from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

import models


def get_or_create_inventory(db: Session, warehouse_id: int, product_id: int) -> models.Inventory:
    inventory = (
        db.query(models.Inventory)
        .filter(
            models.Inventory.warehouse_id == warehouse_id,
            models.Inventory.product_id == product_id,
        )
        .first()
    )
    if inventory is None:
        inventory = models.Inventory(warehouse_id=warehouse_id, product_id=product_id, quantity_on_hand=0)
        db.add(inventory)
        db.flush()
    return inventory


def check_sufficient_stock(db: Session, warehouse_id: int, items: list[tuple[int, int]]) -> None:
    """Raise 400 if any (product_id, quantity) pair exceeds what's on hand in warehouse_id."""
    for product_id, quantity in items:
        inventory = (
            db.query(models.Inventory)
            .filter(
                models.Inventory.warehouse_id == warehouse_id,
                models.Inventory.product_id == product_id,
            )
            .first()
        )
        on_hand = inventory.quantity_on_hand if inventory else 0
        if on_hand < quantity:
            product = db.get(models.Product, product_id)
            name = product.product_name if product else f"product {product_id}"
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {name}: have {on_hand}, need {quantity}",
            )


def adjust_inventory(
    db: Session,
    warehouse_id: int,
    product_id: int,
    delta: int,
    transaction_type: str,
    reference_type: str,
    reference_id: int,
    performed_by: Optional[int],
    notes: Optional[str] = None,
) -> models.Inventory:
    inventory = get_or_create_inventory(db, warehouse_id, product_id)
    inventory.quantity_on_hand += delta
    db.add(
        models.InventoryLog(
            inventory_id=inventory.id,
            transaction_type=transaction_type,
            quantity_change=delta,
            reference_type=reference_type,
            reference_id=reference_id,
            performed_by=performed_by,
            notes=notes,
        )
    )
    return inventory
