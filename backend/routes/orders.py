from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from routes.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


def _get_order_or_404(db: Session, order_id: int) -> models.Order:
    order = db.get(models.Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def _recompute_total(order: models.Order) -> None:
    order.total_amount = sum(float(item.quantity) * float(item.selling_price) for item in order.items)


@router.get("", response_model=list[schemas.OrderRead])
def list_orders(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(models.Order).order_by(models.Order.id.desc()).all()


@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return _get_order_or_404(db, order_id)


@router.post("", response_model=schemas.OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(body: schemas.OrderCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    order = models.Order(customer_id=body.customer_id)
    order.items = [models.OrderItem(**item.model_dump()) for item in body.items]
    _recompute_total(order)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.put("/{order_id}", response_model=schemas.OrderRead)
def update_order(
    order_id: int, body: schemas.OrderCreate, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    order = _get_order_or_404(db, order_id)
    order.customer_id = body.customer_id
    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    order = _get_order_or_404(db, order_id)
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending orders can be deleted")
    db.delete(order)
    db.commit()


@router.post("/{order_id}/items", response_model=schemas.OrderItemRead, status_code=status.HTTP_201_CREATED)
def add_order_item(
    order_id: int, body: schemas.OrderItemCreate, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    order = _get_order_or_404(db, order_id)
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Cannot add items to an order that isn't pending")
    item = models.OrderItem(order_id=order_id, **body.model_dump())
    db.add(item)
    db.flush()
    _recompute_total(order)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{order_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_order_item(order_id: int, item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    order = _get_order_or_404(db, order_id)
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Cannot remove items from an order that isn't pending")
    item = db.get(models.OrderItem, item_id)
    if not item or item.order_id != order_id:
        raise HTTPException(status_code=404, detail="Order item not found")
    db.delete(item)
    db.flush()
    db.refresh(order)
    _recompute_total(order)
    db.commit()


@router.post("/{order_id}/ship", response_model=schemas.ShipmentRead, status_code=status.HTTP_201_CREATED)
def ship_order(
    order_id: int,
    body: schemas.ShipOrderRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Ships this order by calling the sp_ship_order stored procedure, which
    checks the order is pending, checks stock, creates the shipment,
    copies the items over, logs the status, and marks the order processing
    -- all inside the database, in one atomic call.
    """
    try:
        result = db.execute(
            text("SELECT sp_ship_order(:order_id, :warehouse_id, :carrier_id, :tracking)"),
            {
                "order_id": order_id,
                "warehouse_id": body.source_warehouse_id,
                "carrier_id": body.carrier_id,
                "tracking": body.tracking_number,
            },
        )
        shipment_id = result.scalar()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    shipment = db.get(models.Shipment, shipment_id)
    return shipment