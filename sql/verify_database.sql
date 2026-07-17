-- Run in Render's PostgreSQL shell after deployment.

SELECT current_database() AS database_name, current_user AS database_user;

SELECT table_name, row_count
FROM (
    SELECT 'users' AS table_name, COUNT(*) AS row_count FROM users
    UNION ALL SELECT 'categories', COUNT(*) FROM categories
    UNION ALL SELECT 'suppliers', COUNT(*) FROM suppliers
    UNION ALL SELECT 'warehouses', COUNT(*) FROM warehouses
    UNION ALL SELECT 'carriers', COUNT(*) FROM carriers
    UNION ALL SELECT 'customers', COUNT(*) FROM customers
    UNION ALL SELECT 'products', COUNT(*) FROM products
    UNION ALL SELECT 'inventory', COUNT(*) FROM inventory
    UNION ALL SELECT 'purchase_orders', COUNT(*) FROM purchase_orders
    UNION ALL SELECT 'purchase_order_items', COUNT(*) FROM purchase_order_items
    UNION ALL SELECT 'orders', COUNT(*) FROM orders
    UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
    UNION ALL SELECT 'shipments', COUNT(*) FROM shipments
    UNION ALL SELECT 'shipment_items', COUNT(*) FROM shipment_items
    UNION ALL SELECT 'inventory_logs', COUNT(*) FROM inventory_logs
    UNION ALL SELECT 'shipment_status_history', COUNT(*) FROM shipment_status_history
) counts
ORDER BY table_name;
