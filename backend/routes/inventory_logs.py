from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from routes.auth import get_current_user

router = APIRouter(prefix="/inventory-logs", tags=["inventory logs"])


@router.get("", response_model=list[schemas.InventoryLogRead])
def list_inventory_logs(
    inventory_id: Optional[int] = None,
    reference_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.InventoryLog).filter(models.InventoryLog.performed_by == current_user.id)
    if inventory_id is not None:
        query = query.filter(models.InventoryLog.inventory_id == inventory_id)
    if reference_type is not None:
        query = query.filter(models.InventoryLog.reference_type == reference_type)
    return query.order_by(models.InventoryLog.log_timestamp.desc()).all()
