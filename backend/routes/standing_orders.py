from collections import defaultdict
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from routes.auth import get_current_user

router = APIRouter(prefix="/standing-orders", tags=["standing orders"])


def _get_owned_standing_order_or_404(db: Session, standing_order_id: int, user_id: int) -> models.StandingOrder:
    standing_order = (
        db.query(models.StandingOrder)
        .filter(models.StandingOrder.id == standing_order_id, models.StandingOrder.user_id == user_id)
        .first()
    )
    if not standing_order:
        raise HTTPException(status_code=404, detail="Standing order not found")
    return standing_order


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


def _recompute_total(order: models.Order) -> None:
    order.total_amount = sum(float(item.quantity) * float(item.selling_price) for item in order.items)


@router.get("", response_model=list[schemas.StandingOrderRead])
def list_standing_orders(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return (
        db.query(models.StandingOrder)
        .filter(models.StandingOrder.user_id == current_user.id)
        .order_by(models.StandingOrder.id.desc())
        .all()
    )


@router.get("/{standing_order_id}", response_model=schemas.StandingOrderRead)
def get_standing_order(
    standing_order_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return _get_owned_standing_order_or_404(db, standing_order_id, current_user.id)


@router.post("", response_model=schemas.StandingOrderRead, status_code=status.HTTP_201_CREATED)
def create_standing_order(
    body: schemas.StandingOrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    _get_owned_customer_or_404(db, body.customer_id, current_user.id)
    for item in body.items:
        _get_owned_product_or_404(db, item.product_id, current_user.id)

    standing_order = models.StandingOrder(
        user_id=current_user.id,
        customer_id=body.customer_id,
        delivery_frequency_days=body.delivery_frequency_days,
        billing_frequency_days=body.billing_frequency_days,
        start_date=body.start_date,
        next_delivery_date=body.start_date,
        next_billing_date=body.start_date + timedelta(days=body.billing_frequency_days),
    )
    standing_order.items = [models.StandingOrderItem(**item.model_dump()) for item in body.items]
    db.add(standing_order)
    db.commit()
    db.refresh(standing_order)
    return standing_order


@router.put("/{standing_order_id}", response_model=schemas.StandingOrderRead)
def update_standing_order(
    standing_order_id: int,
    body: schemas.StandingOrderUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    standing_order = _get_owned_standing_order_or_404(db, standing_order_id, current_user.id)
    if body.status is not None:
        if body.status not in ("active", "paused", "cancelled"):
            raise HTTPException(status_code=400, detail="status must be active, paused, or cancelled")
        standing_order.status = body.status
    if body.delivery_frequency_days is not None:
        standing_order.delivery_frequency_days = body.delivery_frequency_days
    if body.billing_frequency_days is not None:
        standing_order.billing_frequency_days = body.billing_frequency_days
    db.commit()
    db.refresh(standing_order)
    return standing_order


@router.delete("/{standing_order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_standing_order(
    standing_order_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    standing_order = _get_owned_standing_order_or_404(db, standing_order_id, current_user.id)
    has_orders = db.query(models.Order).filter(models.Order.standing_order_id == standing_order_id).first()
    if has_orders:
        raise HTTPException(
            status_code=400,
            detail="This standing order has already generated orders -- cancel it instead of deleting",
        )
    db.delete(standing_order)
    db.commit()


@router.post(
    "/{standing_order_id}/items",
    response_model=schemas.StandingOrderItemRead,
    status_code=status.HTTP_201_CREATED,
)
def add_standing_order_item(
    standing_order_id: int,
    body: schemas.StandingOrderItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    standing_order = _get_owned_standing_order_or_404(db, standing_order_id, current_user.id)
    if standing_order.status == "cancelled":
        raise HTTPException(status_code=400, detail="Cannot add items to a cancelled standing order")
    _get_owned_product_or_404(db, body.product_id, current_user.id)
    item = models.StandingOrderItem(standing_order_id=standing_order_id, **body.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{standing_order_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_standing_order_item(
    standing_order_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    standing_order = _get_owned_standing_order_or_404(db, standing_order_id, current_user.id)
    if standing_order.status == "cancelled":
        raise HTTPException(status_code=400, detail="Cannot remove items from a cancelled standing order")
    item = db.get(models.StandingOrderItem, item_id)
    if not item or item.standing_order_id != standing_order_id:
        raise HTTPException(status_code=404, detail="Standing order item not found")
    db.delete(item)
    db.commit()


@router.post(
    "/{standing_order_id}/release-order", response_model=schemas.OrderRead, status_code=status.HTTP_201_CREATED
)
def release_order(
    standing_order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Releases the next delivery against this standing order: creates a
    normal Order (tagged with standing_order_id) from the agreed item
    list, and advances next_delivery_date. There's no background
    scheduler in this project, so this is triggered on demand rather
    than by a cron job -- the resulting order flows through the exact
    same fulfillment/shipping endpoints as any other order.
    """
    standing_order = _get_owned_standing_order_or_404(db, standing_order_id, current_user.id)
    if standing_order.status != "active":
        raise HTTPException(status_code=400, detail="Only an active standing order can release an order")
    if not standing_order.items:
        raise HTTPException(status_code=400, detail="Standing order has no items agreed yet")

    order = models.Order(customer_id=standing_order.customer_id, standing_order_id=standing_order.id)
    order.items = [
        models.OrderItem(
            product_id=item.product_id,
            quantity=item.quantity_per_delivery,
            selling_price=item.unit_price,
        )
        for item in standing_order.items
    ]
    _recompute_total(order)
    db.add(order)
    standing_order.next_delivery_date = standing_order.next_delivery_date + timedelta(
        days=standing_order.delivery_frequency_days
    )
    db.commit()
    db.refresh(order)
    return order


@router.post(
    "/{standing_order_id}/generate-invoice",
    response_model=schemas.InvoiceRead,
    status_code=status.HTTP_201_CREATED,
)
def generate_invoice(
    standing_order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Bills the customer for every order this standing order has released
    since it was last billed. This is the piece that decouples billing
    cadence from delivery cadence -- deliveries can happen every week
    while invoices only get generated (and this endpoint only needs
    calling) once a month.

    The invoice records who (customer) and what (one line per product,
    quantities summed across the covered orders) is being billed, not
    just a lump total.
    """
    standing_order = _get_owned_standing_order_or_404(db, standing_order_id, current_user.id)
    unbilled_orders = (
        db.query(models.Order)
        .filter(models.Order.standing_order_id == standing_order_id, models.Order.invoice_id.is_(None))
        .all()
    )
    if not unbilled_orders:
        raise HTTPException(status_code=400, detail="No unbilled orders to invoice for this standing order")

    line_items = defaultdict(lambda: {"quantity": 0, "unit_price": 0})
    for order in unbilled_orders:
        for item in order.items:
            entry = line_items[item.product_id]
            entry["quantity"] += item.quantity
            entry["unit_price"] = item.selling_price

    total = sum(float(entry["quantity"]) * float(entry["unit_price"]) for entry in line_items.values())
    period_start = standing_order.next_billing_date - timedelta(days=standing_order.billing_frequency_days)
    today = date.today()

    invoice = models.Invoice(
        user_id=current_user.id,
        standing_order_id=standing_order.id,
        customer_id=standing_order.customer_id,
        billing_period_start=period_start,
        billing_period_end=today,
        due_date=today + timedelta(days=14),
        total_amount=total,
    )
    db.add(invoice)
    db.flush()

    for product_id, entry in line_items.items():
        db.add(
            models.InvoiceItem(
                invoice_id=invoice.id,
                product_id=product_id,
                quantity=entry["quantity"],
                unit_price=entry["unit_price"],
            )
        )

    for order in unbilled_orders:
        order.invoice_id = invoice.id

    standing_order.next_billing_date = standing_order.next_billing_date + timedelta(
        days=standing_order.billing_frequency_days
    )
    db.commit()
    db.refresh(invoice)
    return invoice
