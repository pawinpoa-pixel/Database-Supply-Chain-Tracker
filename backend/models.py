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
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    parent_category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    color_hex = Column(String(7), nullable=True, default="#4361ee")

    products = relationship("Product", back_populates="category")
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String(150), nullable=False)
    contact_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(30), nullable=True)
    address = Column(Text, nullable=True)

    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    warehouse_name = Column(String(150), nullable=False)
    address = Column(Text, nullable=True)
    capacity = Column(Integer, nullable=True)

    inventory = relationship("Inventory", back_populates="warehouse")


class Carrier(Base):
    __tablename__ = "carriers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    carrier_name = Column(String(150), nullable=False)
    phone = Column(String(30), nullable=True)
    email = Column(String(100), nullable=True)

    shipments = relationship("Shipment", back_populates="carrier")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    customer_name = Column(String(150), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(30), nullable=True)
    address = Column(Text, nullable=True)

    orders = relationship("Order", back_populates="customer")


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("user_id", "sku", name="uq_products_user_sku"),
        UniqueConstraint("user_id", "barcode", name="uq_products_user_barcode"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sku = Column(String(50), nullable=False, index=True)
    product_name = Column(String(150), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    brand = Column(String(100), nullable=True)
    barcode = Column(String(64), nullable=True)
    description = Column(Text, nullable=True)
    unit_of_measure = Column(String(20), nullable=True, default="EA")
    unit_price = Column(Numeric(10, 2), nullable=False, default=0)
    weight_kg = Column(Numeric(10, 3), nullable=True)
    primary_supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    reorder_level = Column(Integer, nullable=False, default=0)
    max_stock_level = Column(Integer, nullable=True)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    category = relationship("Category", back_populates="products")
    primary_supplier = relationship("Supplier")


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
    standing_order_id = Column(Integer, ForeignKey("standing_orders.id"), nullable=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    shipments = relationship("Shipment", back_populates="order")
    standing_order = relationship("StandingOrder", back_populates="orders")
    invoice = relationship("Invoice", back_populates="orders")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")


class StandingOrder(Base):
    """
    A customer's standing arrangement for periodic deliveries against
    one agreement (e.g. "1 case of milk every week for a year"), with
    delivery and billing on independent cadences -- standard
    procurement/ERP terminology (also called a blanket order).

    Each delivery cycle auto-generates a real Order/OrderItem row (see
    Order.standing_order_id) -- it goes through the exact same
    fulfillment/shipping path as any one-off order. Billing is handled
    separately by Invoice, which is what lets "deliver weekly, bill
    monthly" work.
    """

    __tablename__ = "standing_orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    status = Column(String(20), nullable=False, default="active")  # active | paused | cancelled
    delivery_frequency_days = Column(Integer, nullable=False)
    billing_frequency_days = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    next_delivery_date = Column(Date, nullable=False)
    next_billing_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer")
    items = relationship("StandingOrderItem", back_populates="standing_order", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="standing_order")
    invoices = relationship("Invoice", back_populates="standing_order")


class StandingOrderItem(Base):
    __tablename__ = "standing_order_items"

    id = Column(Integer, primary_key=True, index=True)
    standing_order_id = Column(Integer, ForeignKey("standing_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity_per_delivery = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    standing_order = relationship("StandingOrder", back_populates="items")
    product = relationship("Product")


class Invoice(Base):
    """
    A bill: who owes it (customer), what it's for (items, itemized by
    product), and how much (total_amount). Covers one billing period of
    one standing order, aggregating whichever of that standing order's
    generated orders haven't been billed yet (order.invoice_id gets set
    once they're billed) -- this is the piece that lets delivery cadence
    and billing cadence differ.
    """

    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    standing_order_id = Column(Integer, ForeignKey("standing_orders.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    billing_period_start = Column(Date, nullable=False)
    billing_period_end = Column(Date, nullable=False)
    issue_date = Column(Date, nullable=False, server_default=func.current_date())
    due_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="pending")  # pending | paid | overdue | cancelled
    total_amount = Column(Numeric(10, 2), nullable=False, default=0)
    paid_at = Column(DateTime(timezone=True), nullable=True)

    standing_order = relationship("StandingOrder", back_populates="invoices")
    customer = relationship("Customer")
    orders = relationship("Order", back_populates="invoice")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(Base):
    """The itemized 'what' on an invoice -- one row per product being billed."""

    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product")


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    shipment_type = Column(String(20), nullable=False)  # 'TRANSFER' or 'CUSTOMER_DELIVERY'
    shipment_date = Column(DateTime(timezone=True), server_default=func.now())
    source_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    destination_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    carrier_id = Column(Integer, ForeignKey("carriers.id"), nullable=True)
    tracking_number = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default="pending")

    source_warehouse = relationship("Warehouse", foreign_keys=[source_warehouse_id])
    destination_warehouse = relationship("Warehouse", foreign_keys=[destination_warehouse_id])
    order = relationship("Order", back_populates="shipments")
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
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    status_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)

    shipment = relationship("Shipment", back_populates="status_history")
    changed_by_user = relationship("User")
