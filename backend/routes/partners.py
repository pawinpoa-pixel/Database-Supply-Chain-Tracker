from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from routes.auth import get_current_user

suppliers_router = APIRouter(prefix="/suppliers", tags=["suppliers"])
customers_router = APIRouter(prefix="/customers", tags=["customers"])
carriers_router = APIRouter(prefix="/carriers", tags=["carriers"])


@suppliers_router.get("", response_model=list[schemas.SupplierRead])
def list_suppliers(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return (
        db.query(models.Supplier)
        .filter(models.Supplier.user_id == current_user.id)
        .order_by(models.Supplier.id)
        .all()
    )


@suppliers_router.post("", response_model=schemas.SupplierRead, status_code=status.HTTP_201_CREATED)
def create_supplier(
    body: schemas.SupplierCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    supplier = models.Supplier(**body.model_dump(), user_id=current_user.id)
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@suppliers_router.put("/{supplier_id}", response_model=schemas.SupplierRead)
def update_supplier(
    supplier_id: int,
    body: schemas.SupplierCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    supplier = (
        db.query(models.Supplier)
        .filter(models.Supplier.id == supplier_id, models.Supplier.user_id == current_user.id)
        .first()
    )
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    for key, value in body.model_dump().items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return supplier


@suppliers_router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    supplier = (
        db.query(models.Supplier)
        .filter(models.Supplier.id == supplier_id, models.Supplier.user_id == current_user.id)
        .first()
    )
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(supplier)
    db.commit()


@customers_router.get("", response_model=list[schemas.CustomerRead])
def list_customers(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return (
        db.query(models.Customer)
        .filter(models.Customer.user_id == current_user.id)
        .order_by(models.Customer.id)
        .all()
    )


@customers_router.post("", response_model=schemas.CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(
    body: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    customer = models.Customer(**body.model_dump(), user_id=current_user.id)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@customers_router.put("/{customer_id}", response_model=schemas.CustomerRead)
def update_customer(
    customer_id: int,
    body: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    customer = (
        db.query(models.Customer)
        .filter(models.Customer.id == customer_id, models.Customer.user_id == current_user.id)
        .first()
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in body.model_dump().items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer


@customers_router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    customer = (
        db.query(models.Customer)
        .filter(models.Customer.id == customer_id, models.Customer.user_id == current_user.id)
        .first()
    )
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()


@carriers_router.get("", response_model=list[schemas.CarrierRead])
def list_carriers(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return (
        db.query(models.Carrier)
        .filter(models.Carrier.user_id == current_user.id)
        .order_by(models.Carrier.id)
        .all()
    )


@carriers_router.post("", response_model=schemas.CarrierRead, status_code=status.HTTP_201_CREATED)
def create_carrier(
    body: schemas.CarrierCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    carrier = models.Carrier(**body.model_dump(), user_id=current_user.id)
    db.add(carrier)
    db.commit()
    db.refresh(carrier)
    return carrier


@carriers_router.put("/{carrier_id}", response_model=schemas.CarrierRead)
def update_carrier(
    carrier_id: int,
    body: schemas.CarrierCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    carrier = (
        db.query(models.Carrier)
        .filter(models.Carrier.id == carrier_id, models.Carrier.user_id == current_user.id)
        .first()
    )
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    for key, value in body.model_dump().items():
        setattr(carrier, key, value)
    db.commit()
    db.refresh(carrier)
    return carrier


@carriers_router.delete("/{carrier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_carrier(
    carrier_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    carrier = (
        db.query(models.Carrier)
        .filter(models.Carrier.id == carrier_id, models.Carrier.user_id == current_user.id)
        .first()
    )
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    db.delete(carrier)
    db.commit()
