from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from routes.auth import get_current_user
from routes.warehouses import _get_owned_warehouse_or_404

router = APIRouter(prefix="/orders", tags=["orders"])


def _get_owned_customer_or_404(db: Session, customer_id: int, user_id: int) -> models.Customer:
    customer = (
        db.query(models.Customer)
        .filter(models.Customer.id == customer_id, models.Customer.user_id == user_id)
        .first()
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


def _get_owned_product_or_404(db: Session, product_id: int, user_id: int) -> models.Product:
    product = (
        db.query(models.Product)
        .filter(models.Product.id == product_id, models.Product.user_id == user_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def _get_owned_carrier_or_404(db: Session, carrier_id: int, user_id: int) -> models.Carrier:
    carrier = (
        db.query(models.Carrier)
        .filter(models.Carrier.id == carrier_id, models.Carrier.user_id == user_id)
        .first()
    )
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    return carrier


def _get_order_or_404(db: Session, order_id: int, user_id: int) -> models.Order:
    order = (
        db.query(models.Order)
        .join(models.Customer, models.Order.customer_id == models.Customer.id)
        .filter(models.Order.id == order_id, models.Customer.user_id == user_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def _recompute_total(order: models.Order) -> None:
    order.total_amount = sum(float(item.quantity) * float(item.selling_price) for item in order.items)


@router.get("", response_model=list[schemas.OrderRead])
def list_orders(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return (
        db.query(models.Order)
        .join(models.Customer, models.Order.customer_id == models.Customer.id)
        .filter(models.Customer.user_id == current_user.id)
        .order_by(models.Order.id.desc())
        .all()
    )


@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_order(
    order_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return _get_order_or_404(db, order_id, current_user.id)


@router.post("", response_model=schemas.OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(
    body: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    _get_owned_customer_or_404(db, body.customer_id, current_user.id)
    for item in body.items:
        _get_owned_product_or_404(db, item.product_id, current_user.id)
    order = models.Order(customer_id=body.customer_id)
    order.items = [models.OrderItem(**item.model_dump()) for item in body.items]
    _recompute_total(order)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.put("/{order_id}", response_model=schemas.OrderRead)
def update_order(
    order_id: int,
    body: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    order = _get_order_or_404(db, order_id, current_user.id)
    _get_owned_customer_or_404(db, body.customer_id, current_user.id)
    order.customer_id = body.customer_id
    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    order = _get_order_or_404(db, order_id, current_user.id)
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending orders can be deleted")
    db.delete(order)
    db.commit()


@router.post("/{order_id}/items", response_model=schemas.OrderItemRead, status_code=status.HTTP_201_CREATED)
def add_order_item(
    order_id: int,
    body: schemas.OrderItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    order = _get_order_or_404(db, order_id, current_user.id)
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Cannot add items to an order that isn't pending")
    _get_owned_product_or_404(db, body.product_id, current_user.id)
    item = models.OrderItem(order_id=order_id, **body.model_dump())
    db.add(item)
    db.flush()
    _recompute_total(order)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{order_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_order_item(
    order_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    order = _get_order_or_404(db, order_id, current_user.id)
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

    The stored procedure has no concept of users, so ownership of the
    order, warehouse, and carrier must all be validated here first --
    otherwise any authenticated user could ship any other user's order.
    """
    _get_order_or_404(db, order_id, current_user.id)
    _get_owned_warehouse_or_404(db, body.source_warehouse_id, current_user.id)
    if body.carrier_id is not None:
        _get_owned_carrier_or_404(db, body.carrier_id, current_user.id)

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
