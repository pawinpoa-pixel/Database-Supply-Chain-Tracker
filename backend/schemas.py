from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ChangePassword(BaseModel):
    current_password: str
    new_password: str


# ---- Categories ----

class CategoryCreate(BaseModel):
    category_name: str
    description: Optional[str] = None

class CategoryRead(CategoryCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---- Suppliers ----

class SupplierCreate(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class SupplierRead(SupplierCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---- Warehouses ----

class WarehouseCreate(BaseModel):
    warehouse_name: str
    address: Optional[str] = None
    capacity: Optional[int] = None

class WarehouseRead(WarehouseCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---- Carriers ----

class CarrierCreate(BaseModel):
    carrier_name: str
    phone: Optional[str] = None
    email: Optional[str] = None

class CarrierRead(CarrierCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---- Customers ----

class CustomerCreate(BaseModel):
    customer_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerRead(CustomerCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---- Products ----

class ProductCreate(BaseModel):
    sku: str
    product_name: str
    category_id: Optional[int] = None
    unit_price: float
    reorder_level: int = 0
    is_active: bool = True

class ProductRead(ProductCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    category: Optional[CategoryRead] = None


# ---- Inventory ----

class InventoryCreate(BaseModel):
    warehouse_id: int
    product_id: int
    quantity_on_hand: int = 0

class InventoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    warehouse_id: int
    product_id: int
    quantity_on_hand: int
    last_updated: Optional[datetime] = None
    warehouse: WarehouseRead
    product: ProductRead


# ---- Purchase Orders ----

class PurchaseOrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_cost: float

class PurchaseOrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    po_id: int
    product_id: int
    quantity: int
    unit_cost: float
    product: ProductRead

class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    expected_delivery_date: Optional[date] = None
    items: list[PurchaseOrderItemCreate] = []

class PurchaseOrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    supplier_id: int
    order_date: Optional[datetime] = None
    expected_delivery_date: Optional[date] = None
    status: str
    supplier: SupplierRead
    items: list[PurchaseOrderItemRead] = []

class ReceivePORequest(BaseModel):
    warehouse_id: int


# ---- Orders ----

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    selling_price: float

class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_id: int
    product_id: int
    quantity: int
    selling_price: float
    product: ProductRead

class OrderCreate(BaseModel):
    customer_id: int
    items: list[OrderItemCreate] = []

class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer_id: int
    order_date: Optional[datetime] = None
    status: str
    total_amount: float
    customer: CustomerRead
    items: list[OrderItemRead] = []

class FulfillOrderRequest(BaseModel):
    warehouse_id: int


# ---- Shipments ----

class ShipmentItemCreate(BaseModel):
    product_id: int
    quantity: int

class ShipmentItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    shipment_id: int
    product_id: int
    quantity: int
    product: ProductRead

class ShipmentCreate(BaseModel):
    source_warehouse_id: int
    destination_warehouse_id: int
    carrier_id: Optional[int] = None
    tracking_number: Optional[str] = None
    items: list[ShipmentItemCreate] = []

class ShipmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    shipment_date: Optional[datetime] = None
    source_warehouse_id: int
    destination_warehouse_id: int
    carrier_id: Optional[int] = None
    tracking_number: Optional[str] = None
    status: str
    source_warehouse: WarehouseRead
    destination_warehouse: WarehouseRead
    carrier: Optional[CarrierRead] = None
    items: list[ShipmentItemRead] = []

class ShipmentStatusHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    shipment_id: int
    status: str
    location: Optional[str] = None
    status_timestamp: Optional[datetime] = None
    notes: Optional[str] = None


# ---- Inventory logs (read-only ledger) ----

class InventoryLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    inventory_id: int
    transaction_type: str
    quantity_change: int
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    performed_by: Optional[int] = None
    log_timestamp: Optional[datetime] = None
    notes: Optional[str] = None
