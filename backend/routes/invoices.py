from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from routes.auth import get_current_user

router = APIRouter(prefix="/invoices", tags=["invoices"])


def _get_owned_invoice_or_404(db: Session, invoice_id: int, user_id: int) -> models.Invoice:
    invoice = (
        db.query(models.Invoice)
        .filter(models.Invoice.id == invoice_id, models.Invoice.user_id == user_id)
        .first()
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.get("", response_model=list[schemas.InvoiceRead])
def list_invoices(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return (
        db.query(models.Invoice)
        .filter(models.Invoice.user_id == current_user.id)
        .order_by(models.Invoice.id.desc())
        .all()
    )


@router.get("/{invoice_id}", response_model=schemas.InvoiceRead)
def get_invoice(
    invoice_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return _get_owned_invoice_or_404(db, invoice_id, current_user.id)


@router.post("/{invoice_id}/pay", response_model=schemas.InvoiceRead)
def pay_invoice(
    invoice_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    invoice = _get_owned_invoice_or_404(db, invoice_id, current_user.id)
    if invoice.status != "pending":
        raise HTTPException(status_code=400, detail=f"Invoice is already {invoice.status}")
    invoice.status = "paid"
    invoice.paid_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(invoice)
    return invoice
