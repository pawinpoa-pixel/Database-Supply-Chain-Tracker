from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from inventory_utils import adjust_inventory
from routes.auth import get_current_user
from routes.warehouses import _get_owned_warehouse_or_404

router = APIRouter(prefix="/purchase-orders", tags=["purchase orders"])


def _get_owned_supplier_or_404(db: Session, supplier_id: int, user_id: int) -> models.Supplier:
    supplier = (
        db.query(models.Supplier)
        .filter(models.Supplier.id == supplier_id, models.Supplier.user_id == user_id)
        .first()
    )
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


def _get_owned_product_or_404(db: Session, product_id: int, user_id: int) -> models.Product:
    product = (
        db.query(models.Product)
        .filter(models.Product.id == product_id, models.Product.user_id == user_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def _get_po_or_404(db: Session, po_id: int, user_id: int) -> models.PurchaseOrder:
    po = (
        db.query(models.PurchaseOrder)
        .join(models.Supplier, models.PurchaseOrder.supplier_id == models.Supplier.id)
        .filter(models.PurchaseOrder.id == po_id, models.Supplier.user_id == user_id)
        .first()
    )
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return po


@router.get("", response_model=list[schemas.PurchaseOrderRead])
def list_purchase_orders(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return (
        db.query(models.PurchaseOrder)
        .join(models.Supplier, models.PurchaseOrder.supplier_id == models.Supplier.id)
        .filter(models.Supplier.user_id == current_user.id)
        .order_by(models.PurchaseOrder.id.desc())
        .all()
    )


@router.get("/{po_id}", response_model=schemas.PurchaseOrderRead)
def get_purchase_order(
    po_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return _get_po_or_404(db, po_id, current_user.id)


@router.post("", response_model=schemas.PurchaseOrderRead, status_code=status.HTTP_201_CREATED)
def create_purchase_order(
    body: schemas.PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    _get_owned_supplier_or_404(db, body.supplier_id, current_user.id)
    for item in body.items:
        _get_owned_product_or_404(db, item.product_id, current_user.id)
    po = models.PurchaseOrder(
        supplier_id=body.supplier_id,
        expected_delivery_date=body.expected_delivery_date,
    )
    po.items = [models.PurchaseOrderItem(**item.model_dump()) for item in body.items]
    db.add(po)
    db.commit()
    db.refresh(po)
    return po


@router.put("/{po_id}", response_model=schemas.PurchaseOrderRead)
def update_purchase_order(
    po_id: int,
    body: schemas.PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    po = _get_po_or_404(db, po_id, current_user.id)
    _get_owned_supplier_or_404(db, body.supplier_id, current_user.id)
    po.supplier_id = body.supplier_id
    po.expected_delivery_date = body.expected_delivery_date
    db.commit()
    db.refresh(po)
    return po


@router.delete("/{po_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase_order(
    po_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    po = _get_po_or_404(db, po_id, current_user.id)
    if po.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending purchase orders can be deleted")
    db.delete(po)
    db.commit()


@router.post("/{po_id}/items", response_model=schemas.PurchaseOrderItemRead, status_code=status.HTTP_201_CREATED)
def add_purchase_order_item(
    po_id: int,
    body: schemas.PurchaseOrderItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    po = _get_po_or_404(db, po_id, current_user.id)
    if po.status != "pending":
        raise HTTPException(status_code=400, detail="Cannot add items to a purchase order that isn't pending")
    _get_owned_product_or_404(db, body.product_id, current_user.id)
    item = models.PurchaseOrderItem(po_id=po_id, **body.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{po_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_purchase_order_item(
    po_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    po = _get_po_or_404(db, po_id, current_user.id)
    if po.status != "pending":
        raise HTTPException(status_code=400, detail="Cannot remove items from a purchase order that isn't pending")
    item = db.get(models.PurchaseOrderItem, item_id)
    if not item or item.po_id != po_id:
        raise HTTPException(status_code=404, detail="Purchase order item not found")
    db.delete(item)
    db.commit()


@router.post("/{po_id}/receive", response_model=schemas.PurchaseOrderRead)
def receive_purchase_order(
    po_id: int,
    body: schemas.ReceivePORequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    po = _get_po_or_404(db, po_id, current_user.id)
    if po.status != "pending":
        raise HTTPException(status_code=400, detail="Purchase order has already been received or cancelled")
    if not po.items:
        raise HTTPException(status_code=400, detail="Purchase order has no items to receive")
    _get_owned_warehouse_or_404(db, body.warehouse_id, current_user.id)

    for item in po.items:
        adjust_inventory(
            db,
            warehouse_id=body.warehouse_id,
            product_id=item.product_id,
            delta=item.quantity,
            transaction_type="po_receipt",
            reference_type="purchase_order",
            reference_id=po.id,
            performed_by=current_user.id,
        )

    po.status = "received"
    db.commit()
    db.refresh(po)
    return po
