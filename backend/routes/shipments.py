from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from inventory_utils import adjust_inventory, check_sufficient_stock
from routes.auth import get_current_user

router = APIRouter(prefix="/shipments", tags=["shipments"])


def _get_shipment_or_404(db: Session, shipment_id: int) -> models.Shipment:
    shipment = db.get(models.Shipment, shipment_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@router.get("", response_model=list[schemas.ShipmentRead])
def list_shipments(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(models.Shipment).order_by(models.Shipment.id.desc()).all()


@router.get("/{shipment_id}", response_model=schemas.ShipmentRead)
def get_shipment(shipment_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return _get_shipment_or_404(db, shipment_id)


@router.get("/{shipment_id}/history", response_model=list[schemas.ShipmentStatusHistoryRead])
def get_shipment_history(shipment_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    _get_shipment_or_404(db, shipment_id)
    return (
        db.query(models.ShipmentStatusHistory)
        .filter(models.ShipmentStatusHistory.shipment_id == shipment_id)
        .order_by(models.ShipmentStatusHistory.status_timestamp)
        .all()
    )


@router.post("", response_model=schemas.ShipmentRead, status_code=status.HTTP_201_CREATED)
def create_shipment(body: schemas.ShipmentCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if body.source_warehouse_id == body.destination_warehouse_id:
        raise HTTPException(status_code=400, detail="Source and destination warehouse must differ")

    shipment = models.Shipment(
        source_warehouse_id=body.source_warehouse_id,
        destination_warehouse_id=body.destination_warehouse_id,
        carrier_id=body.carrier_id,
        tracking_number=body.tracking_number,
    )
    shipment.items = [models.ShipmentItem(**item.model_dump()) for item in body.items]
    db.add(shipment)
    db.flush()
    db.add(models.ShipmentStatusHistory(shipment_id=shipment.id, status="pending"))
    db.commit()
    db.refresh(shipment)
    return shipment


@router.put("/{shipment_id}", response_model=schemas.ShipmentRead)
def update_shipment(
    shipment_id: int,
    body: schemas.ShipmentCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    shipment = _get_shipment_or_404(db, shipment_id)
    if shipment.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending shipments can be edited")
    if body.source_warehouse_id == body.destination_warehouse_id:
        raise HTTPException(status_code=400, detail="Source and destination warehouse must differ")
    shipment.source_warehouse_id = body.source_warehouse_id
    shipment.destination_warehouse_id = body.destination_warehouse_id
    shipment.carrier_id = body.carrier_id
    shipment.tracking_number = body.tracking_number
    db.commit()
    db.refresh(shipment)
    return shipment


@router.delete("/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipment(shipment_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    shipment = _get_shipment_or_404(db, shipment_id)
    if shipment.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending shipments can be deleted")
    db.delete(shipment)
    db.commit()


@router.post("/{shipment_id}/items", response_model=schemas.ShipmentItemRead, status_code=status.HTTP_201_CREATED)
def add_shipment_item(
    shipment_id: int,
    body: schemas.ShipmentItemCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    shipment = _get_shipment_or_404(db, shipment_id)
    if shipment.status != "pending":
        raise HTTPException(status_code=400, detail="Cannot add items to a shipment that isn't pending")
    item = models.ShipmentItem(shipment_id=shipment_id, **body.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{shipment_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_shipment_item(
    shipment_id: int, item_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    shipment = _get_shipment_or_404(db, shipment_id)
    if shipment.status != "pending":
        raise HTTPException(status_code=400, detail="Cannot remove items from a shipment that isn't pending")
    item = db.get(models.ShipmentItem, item_id)
    if not item or item.shipment_id != shipment_id:
        raise HTTPException(status_code=404, detail="Shipment item not found")
    db.delete(item)
    db.commit()


@router.post("/{shipment_id}/ship", response_model=schemas.ShipmentRead)
def ship_shipment(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    shipment = _get_shipment_or_404(db, shipment_id)
    if shipment.status != "pending":
        raise HTTPException(status_code=400, detail="Only a pending shipment can be shipped")
    if not shipment.items:
        raise HTTPException(status_code=400, detail="Shipment has no items to ship")

    check_sufficient_stock(
        db, shipment.source_warehouse_id, [(item.product_id, item.quantity) for item in shipment.items]
    )

    for item in shipment.items:
        adjust_inventory(
            db,
            warehouse_id=shipment.source_warehouse_id,
            product_id=item.product_id,
            delta=-item.quantity,
            transaction_type="shipment_out",
            reference_type="shipment",
            reference_id=shipment.id,
            performed_by=current_user.id,
        )

    shipment.status = "in_transit"
    db.add(models.ShipmentStatusHistory(shipment_id=shipment.id, status="in_transit"))
    db.commit()
    db.refresh(shipment)
    return shipment


@router.post("/{shipment_id}/deliver", response_model=schemas.ShipmentRead)
def deliver_shipment(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    shipment = _get_shipment_or_404(db, shipment_id)
    if shipment.status != "in_transit":
        raise HTTPException(status_code=400, detail="Only an in-transit shipment can be delivered")

    for item in shipment.items:
        adjust_inventory(
            db,
            warehouse_id=shipment.destination_warehouse_id,
            product_id=item.product_id,
            delta=item.quantity,
            transaction_type="shipment_in",
            reference_type="shipment",
            reference_id=shipment.id,
            performed_by=current_user.id,
        )

    shipment.status = "delivered"
    db.add(models.ShipmentStatusHistory(shipment_id=shipment.id, status="delivered"))
    db.commit()
    db.refresh(shipment)
    return shipment
