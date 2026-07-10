-- views.sql
-- Read-only. Safe to run any time. These are your report /
-- dashboard queries pre-packaged for reuse and demo screenshots.


CREATE OR REPLACE VIEW vw_current_inventory AS
SELECT
    w.warehouse_name,
    p.product_name,
    p.sku,
    c.category_name,
    i.quantity_on_hand,
    p.reorder_level,
    i.last_updated
FROM inventory i
JOIN warehouses w ON w.id = i.warehouse_id
JOIN products p ON p.id = i.product_id
LEFT JOIN categories c ON c.id = p.category_id
ORDER BY w.warehouse_name, p.product_name;


CREATE OR REPLACE VIEW vw_low_stock AS
SELECT
    p.id AS product_id,
    p.product_name,
    p.sku,
    SUM(i.quantity_on_hand) AS total_quantity,
    p.reorder_level
FROM products p
JOIN inventory i ON i.product_id = p.id
GROUP BY p.id, p.product_name, p.sku, p.reorder_level
HAVING SUM(i.quantity_on_hand) < p.reorder_level;


CREATE OR REPLACE VIEW vw_order_summary AS
SELECT
    o.id AS order_id,
    cu.customer_name,
    o.status,
    o.order_date,
    o.total_amount,
    COUNT(oi.id) AS item_count
FROM orders o
JOIN customers cu ON cu.id = o.customer_id
LEFT JOIN order_items oi ON oi.order_id = o.id
GROUP BY o.id, cu.customer_name, o.status, o.order_date, o.total_amount
ORDER BY o.order_date DESC;


CREATE OR REPLACE VIEW vw_shipment_tracking AS
SELECT
    s.id AS shipment_id,
    s.shipment_type,
    s.status,
    s.tracking_number,
    sw.warehouse_name AS source_warehouse,
    dw.warehouse_name AS destination_warehouse,
    o.id AS order_id,
    cu.customer_name,
    car.carrier_name,
    s.shipment_date
FROM shipments s
JOIN warehouses sw ON sw.id = s.source_warehouse_id
LEFT JOIN warehouses dw ON dw.id = s.destination_warehouse_id
LEFT JOIN orders o ON o.id = s.order_id
LEFT JOIN customers cu ON cu.id = o.customer_id
LEFT JOIN carriers car ON car.id = s.carrier_id
ORDER BY s.shipment_date DESC;


CREATE OR REPLACE VIEW vw_supplier_performance AS
SELECT
    su.id AS supplier_id,
    su.company_name,
    COUNT(po.id) AS total_purchase_orders,
    COUNT(po.id) FILTER (WHERE po.status = 'received') AS received_count,
    COUNT(po.id) FILTER (WHERE po.status = 'pending') AS pending_count
FROM suppliers su
LEFT JOIN purchase_orders po ON po.supplier_id = su.id
GROUP BY su.id, su.company_name
ORDER BY total_purchase_orders DESC;


CREATE OR REPLACE VIEW vw_product_sales_summary AS
SELECT
    p.id AS product_id,
    p.product_name,
    p.sku,
    COALESCE(SUM(oi.quantity), 0) AS total_units_sold,
    COALESCE(SUM(oi.quantity * oi.selling_price), 0) AS total_revenue
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.id
GROUP BY p.id, p.product_name, p.sku
ORDER BY total_revenue DESC;