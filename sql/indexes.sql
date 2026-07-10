CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);

CREATE INDEX IF NOT EXISTS idx_inventory_product_id ON inventory(product_id);

CREATE INDEX IF NOT EXISTS idx_purchase_orders_supplier_id ON purchase_orders(supplier_id);
CREATE INDEX IF NOT EXISTS idx_purchase_orders_status ON purchase_orders(status);
CREATE INDEX IF NOT EXISTS idx_purchase_order_items_po_id ON purchase_order_items(po_id);
CREATE INDEX IF NOT EXISTS idx_purchase_order_items_product_id ON purchase_order_items(product_id);

CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);

CREATE INDEX IF NOT EXISTS idx_shipments_source_warehouse_id ON shipments(source_warehouse_id);
CREATE INDEX IF NOT EXISTS idx_shipments_destination_warehouse_id ON shipments(destination_warehouse_id);
CREATE INDEX IF NOT EXISTS idx_shipments_order_id ON shipments(order_id);
CREATE INDEX IF NOT EXISTS idx_shipments_carrier_id ON shipments(carrier_id);
CREATE INDEX IF NOT EXISTS idx_shipments_status ON shipments(status);

CREATE INDEX IF NOT EXISTS idx_shipment_items_shipment_id ON shipment_items(shipment_id);
CREATE INDEX IF NOT EXISTS idx_shipment_items_product_id ON shipment_items(product_id);

CREATE INDEX IF NOT EXISTS idx_inventory_logs_inventory_id ON inventory_logs(inventory_id);
CREATE INDEX IF NOT EXISTS idx_inventory_logs_performed_by ON inventory_logs(performed_by);
CREATE INDEX IF NOT EXISTS idx_inventory_logs_reference ON inventory_logs(reference_type, reference_id);

CREATE INDEX IF NOT EXISTS idx_shipment_status_history_shipment_id ON shipment_status_history(shipment_id);