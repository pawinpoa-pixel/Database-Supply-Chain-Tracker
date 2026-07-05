from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    Boolean,
    DateTime,
    Date,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    products = relationship("Product", back_populates="category")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(150), nullable=False)
    contact_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(30), nullable=True)
    address = Column(Text, nullable=True)

    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_name = Column(String(150), nullable=False)
    address = Column(Text, nullable=True)
    capacity = Column(Integer, nullable=True)

    inventory = relationship("Inventory", back_populates="warehouse")


class Carrier(Base):
    __tablename__ = "carriers"

    id = Column(Integer, primary_key=True, index=True)
    carrier_name = Column(String(150), nullable=False)
    phone = Column(String(30), nullable=True)
    email = Column(String(100), nullable=True)

    shipments = relationship("Shipment", back_populates="carrier")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(150), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(30), nullable=True)
    address = Column(Text, nullable=True)

    orders = relationship("Order", back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    product_name = Column(String(150), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    unit_price = Column(Numeric(10, 2), nullable=False, default=0)
    reorder_level = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)

    category = relationship("Category", back_populates="products")


class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = (UniqueConstraint("warehouse_id", "product_id", name="uq_inventory_warehouse_product"),)

    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity_on_hand = Column(Integer, nullable=False, default=0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    warehouse = relationship("Warehouse", back_populates="inventory")
    product = relationship("Product")
    logs = relationship("InventoryLog", back_populates="inventory")


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    expected_delivery_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="pending")

    supplier = relationship("Supplier", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan")


class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"

    id = Column(Integer, primary_key=True, index=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Numeric(10, 2), nullable=False)

    purchase_order = relationship("PurchaseOrder", back_populates="items")
    product = relationship("Product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), nullable=False, default="pending")
    total_amount = Column(Numeric(10, 2), nullable=False, default=0)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    shipment_date = Column(DateTime(timezone=True), server_default=func.now())
    source_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    destination_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    carrier_id = Column(Integer, ForeignKey("carriers.id"), nullable=True)
    tracking_number = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default="pending")

    source_warehouse = relationship("Warehouse", foreign_keys=[source_warehouse_id])
    destination_warehouse = relationship("Warehouse", foreign_keys=[destination_warehouse_id])
    carrier = relationship("Carrier", back_populates="shipments")
    items = relationship("ShipmentItem", back_populates="shipment", cascade="all, delete-orphan")
    status_history = relationship(
        "ShipmentStatusHistory", back_populates="shipment", cascade="all, delete-orphan"
    )


class ShipmentItem(Base):
    __tablename__ = "shipment_items"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    shipment = relationship("Shipment", back_populates="items")
    product = relationship("Product")


class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    transaction_type = Column(String(30), nullable=False)
    quantity_change = Column(Integer, nullable=False)
    reference_type = Column(String(30), nullable=True)
    reference_id = Column(Integer, nullable=True)
    performed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    log_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)

    inventory = relationship("Inventory", back_populates="logs")


class ShipmentStatusHistory(Base):
    __tablename__ = "shipment_status_history"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    status = Column(String(20), nullable=False)
    location = Column(String(150), nullable=True)
    status_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)

    shipment = relationship("Shipment", back_populates="status_history")
