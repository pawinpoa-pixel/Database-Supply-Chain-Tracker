TRUNCATE TABLE
    shipment_status_history,
    inventory_logs,
    shipment_items,
    shipments,
    order_items,
    orders,
    purchase_order_items,
    purchase_orders,
    inventory,
    products,
    users,
    customers,
    carriers,
    warehouses,
    suppliers,
    categories
RESTART IDENTITY CASCADE;

-- ------------------------------------------------------------
-- categories (10)
-- ------------------------------------------------------------
INSERT INTO categories (category_name, description) VALUES
('Beverages', 'Soft drinks, teas, and bottled water'),
('Dairy', 'Milk, cheese, and dairy products'),
('Snacks', 'Chips, nuts, and packaged snacks'),
('Frozen Foods', 'Frozen meals and frozen ingredients'),
('Bakery', 'Bread, pastries, and baked goods'),
('Produce', 'Fresh fruits and vegetables'),
('Meat & Poultry', 'Fresh and packaged meat products'),
('Cleaning Supplies', 'Commercial cleaning products'),
('Personal Care', 'Hygiene and personal care items'),
('Canned Goods', 'Canned and preserved foods');

-- ------------------------------------------------------------
-- suppliers (10)
-- ------------------------------------------------------------
INSERT INTO suppliers (company_name, contact_name, email, phone, address) VALUES
('Golden Valley Beverages Co.', 'Somchai Boonmee', 'sales@goldenvalley.co.th', '02-555-0101', '88 Sukhumvit Rd, Bangkok'),
('Sunrise Dairy Farms', 'Malee Thongchai', 'contact@sunrisedairy.co.th', '02-555-0102', '12 Ratchada Rd, Bangkok'),
('Crunch Time Snacks Ltd.', 'Wichai Ruangsri', 'orders@crunchtime.co.th', '02-555-0103', '45 Silom Rd, Bangkok'),
('Arctic Fresh Frozen Foods', 'Nattaya Chaiyaporn', 'info@arcticfresh.co.th', '02-555-0104', '77 Rama IV Rd, Bangkok'),
('Golden Crust Bakery Supply', 'Preecha Nualsri', 'sales@goldencrust.co.th', '02-555-0105', '23 Phahonyothin Rd, Bangkok'),
('Green Acres Produce', 'Anong Petchara', 'contact@greenacres.co.th', '02-555-0106', '56 Ladprao Rd, Bangkok'),
('Premium Meats Wholesale', 'Kittipong Saelim', 'orders@premiummeats.co.th', '02-555-0107', '34 Bang Na Rd, Bangkok'),
('SparkleClean Supplies Co.', 'Supaporn Kraisri', 'sales@sparkleclean.co.th', '02-555-0108', '19 Charoen Krung Rd, Bangkok'),
('PureCare Personal Products', 'Jaidee Wattana', 'info@purecare.co.th', '02-555-0109', '61 Sathorn Rd, Bangkok'),
('Harvest Best Canned Goods', 'Somsak Uraiwan', 'contact@harvestbest.co.th', '02-555-0110', '8 Petchaburi Rd, Bangkok');

-- ------------------------------------------------------------
-- warehouses (10)
-- ------------------------------------------------------------
INSERT INTO warehouses (warehouse_name, address, capacity) VALUES
('Bangkok Central Warehouse', '100 Bang Phlat, Bangkok', 50000),
('Chiang Mai Distribution Center', '25 Hang Dong Rd, Chiang Mai', 30000),
('Pattaya Coastal Warehouse', '14 Sukhumvit Rd, Pattaya', 20000),
('Khon Kaen Regional Hub', '9 Mittraphap Rd, Khon Kaen', 25000),
('Phuket Storage Facility', '33 Chalermprakiat Rd, Phuket', 15000),
('Nonthaburi Cold Storage', '77 Rattanathibet Rd, Nonthaburi', 18000),
('Rayong Logistics Center', '5 Sukhumvit Rd, Rayong', 22000),
('Udon Thani Warehouse', '41 Prajak Rd, Udon Thani', 17000),
('Hat Yai Southern Hub', '62 Niphat Uthit Rd, Hat Yai', 19000),
('Ayutthaya Overflow Storage', '3 Rojana Rd, Ayutthaya', 12000);

-- ------------------------------------------------------------
-- carriers (10)
-- ------------------------------------------------------------
INSERT INTO carriers (carrier_name, phone, email) VALUES
('Kerry Express', '02-800-4000', 'support@kerryexpress.co.th'),
('Thailand Post', '1545', 'contact@thailandpost.co.th'),
('Flash Express', '1425', 'support@flashexpress.co.th'),
('DHL Thailand', '02-345-5000', 'thailand@dhl.com'),
('J&T Express', '02-460-5988', 'support@jtexpress.co.th'),
('Ninja Van Thailand', '02-006-9696', 'support@ninjavan.co'),
('SCG Express', '02-586-3333', 'contact@scgexpress.co.th'),
('Best Express', '02-116-8999', 'support@best-inc.co.th'),
('Alpha Fast Logistics', '02-222-3344', 'info@alphafast.co.th'),
('Speedy Cargo Co.', '02-333-4455', 'contact@speedycargo.co.th');

-- ------------------------------------------------------------
-- customers (10)
-- ------------------------------------------------------------
INSERT INTO customers (customer_name, email, phone, address) VALUES
('Golden Spoon Restaurant Group', 'purchasing@goldenspoon.co.th', '02-700-1001', '10 Thonglor Rd, Bangkok'),
('QuickBite Convenience Stores', 'orders@quickbite.co.th', '02-700-1002', '22 Ari Rd, Bangkok'),
('Fresh Mart Supermarket', 'supply@freshmart.co.th', '02-700-1003', '5 Ekkamai Rd, Bangkok'),
('Urban Cafe Chain', 'purchasing@urbancafe.co.th', '02-700-1004', '18 Sathorn Rd, Bangkok'),
('Sunny Side Diner', 'orders@sunnyside.co.th', '02-700-1005', '7 Phrom Phong Rd, Bangkok'),
('Metro Grocery Co.', 'supply@metrogrocery.co.th', '02-700-1006', '33 Bangna Rd, Bangkok'),
('Green Leaf Restaurants', 'purchasing@greenleaf.co.th', '02-700-1007', '15 Ratchada Rd, Bangkok'),
('Night Owl 24hr Stores', 'orders@nightowl.co.th', '02-700-1008', '9 Silom Rd, Bangkok'),
('Coastal Kitchen Group', 'purchasing@coastalkitchen.co.th', '038-700-1009', '20 Beach Rd, Pattaya'),
('Big Basket Wholesale Club', 'supply@bigbasket.co.th', '02-700-1010', '44 Ladprao Rd, Bangkok');

-- ------------------------------------------------------------
-- users (10) -- password for all: "Password123!"
-- ------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS pgcrypto;

INSERT INTO users (username, email, password) VALUES
('admin_som', 'som.admin@supplychain.co.th', crypt('Password123!', gen_salt('bf'))),
('jaidee_w', 'jaidee.w@supplychain.co.th', crypt('Password123!', gen_salt('bf'))),
('anong_p', 'anong.p@supplychain.co.th', crypt('Password123!', gen_salt('bf'))),
('kittipong_s', 'kittipong.s@supplychain.co.th', crypt('Password123!', gen_salt('bf'))),
('malee_t', 'malee.t@supplychain.co.th', crypt('Password123!', gen_salt('bf'))),
('preecha_n', 'preecha.n@supplychain.co.th', crypt('Password123!', gen_salt('bf'))),
('supaporn_k', 'supaporn.k@supplychain.co.th', crypt('Password123!', gen_salt('bf'))),
('wichai_r', 'wichai.r@supplychain.co.th', crypt('Password123!', gen_salt('bf'))),
('nattaya_c', 'nattaya.c@supplychain.co.th', crypt('Password123!', gen_salt('bf'))),
('somchai_b', 'somchai.b@supplychain.co.th', crypt('Password123!', gen_salt('bf')));

-- ------------------------------------------------------------
-- products (12) -- category_id references categories above
-- ------------------------------------------------------------
INSERT INTO products (sku, product_name, category_id, unit_price, reorder_level, is_active) VALUES
('BEV-001', 'Thai Iced Tea Concentrate 1L', 1, 89.00, 50, TRUE),
('BEV-002', 'Sparkling Water 500ml (Case of 24)', 1, 240.00, 30, TRUE),
('DAI-001', 'Fresh Milk 1L', 2, 45.00, 80, TRUE),
('DAI-002', 'Cheddar Cheese Block 500g', 2, 165.00, 40, TRUE),
('SNK-001', 'Potato Chips 150g', 3, 35.00, 100, TRUE),
('SNK-002', 'Mixed Nuts 200g', 3, 89.00, 60, TRUE),
('FRZ-001', 'Frozen Chicken Nuggets 1kg', 4, 129.00, 50, TRUE),
('FRZ-002', 'Frozen Mixed Vegetables 1kg', 4, 79.00, 45, TRUE),
('BAK-001', 'White Sandwich Bread', 5, 32.00, 70, TRUE),
('BAK-002', 'Croissants (6-pack)', 5, 99.00, 40, TRUE),
('PRD-001', 'Fresh Tomatoes 1kg', 6, 55.00, 60, TRUE),
('MEA-001', 'Chicken Breast 1kg', 7, 149.00, 50, TRUE);

-- ------------------------------------------------------------
-- inventory (16) -- warehouse_id, product_id must be unique pairs
-- ------------------------------------------------------------
INSERT INTO inventory (warehouse_id, product_id, quantity_on_hand) VALUES
(1, 1, 500), (1, 2, 300), (1, 3, 200), (1, 4, 150), (1, 5, 400),
(2, 1, 250), (2, 3, 180), (2, 6, 220), (2, 7, 90),
(3, 2, 310), (3, 5, 275), (3, 8, 60),
(4, 9, 120), (4, 10, 80),
(5, 11, 140), (5, 12, 95);

-- ------------------------------------------------------------
-- purchase_orders (10) -- supplier_id references suppliers
-- ------------------------------------------------------------
INSERT INTO purchase_orders (supplier_id, expected_delivery_date, status) VALUES
(1, '2026-07-15', 'received'),
(2, '2026-07-16', 'received'),
(3, '2026-07-18', 'pending'),
(4, '2026-07-20', 'pending'),
(5, '2026-07-14', 'received'),
(6, '2026-07-22', 'pending'),
(7, '2026-07-17', 'received'),
(8, '2026-07-25', 'pending'),
(9, '2026-07-19', 'pending'),
(10, '2026-07-21', 'pending');

-- ------------------------------------------------------------
-- purchase_order_items (15)
-- ------------------------------------------------------------
INSERT INTO purchase_order_items (po_id, product_id, quantity, unit_cost) VALUES
(1, 1, 200, 60.00),
(1, 2, 100, 180.00),
(2, 3, 300, 30.00),
(2, 4, 100, 120.00),
(3, 5, 400, 20.00),
(4, 7, 200, 90.00),
(4, 8, 150, 55.00),
(5, 9, 300, 20.00),
(5, 10, 150, 65.00),
(6, 11, 250, 35.00),
(7, 12, 200, 100.00),
(7, 1, 100, 58.00),
(8, 6, 180, 60.00),
(9, 2, 90, 175.00),
(10, 4, 60, 118.00);

-- ------------------------------------------------------------
-- orders (10) -- customer_id references customers
-- ------------------------------------------------------------
INSERT INTO orders (customer_id, status, total_amount) VALUES
(1, 'pending', 0),
(2, 'pending', 0),
(3, 'processing', 0),
(4, 'processing', 0),
(5, 'fulfilled', 0),
(6, 'fulfilled', 0),
(7, 'pending', 0),
(8, 'processing', 0),
(9, 'pending', 0),
(10, 'fulfilled', 0);

-- ------------------------------------------------------------
-- order_items (16) -- total_amount recomputed after
-- ------------------------------------------------------------
INSERT INTO order_items (order_id, product_id, quantity, selling_price) VALUES
(1, 1, 24, 95.00), (1, 5, 40, 38.00),
(2, 3, 30, 48.00),
(3, 2, 12, 250.00), (3, 6, 20, 95.00),
(4, 7, 15, 135.00),
(5, 9, 25, 35.00), (5, 10, 10, 105.00),
(6, 11, 20, 60.00),
(7, 4, 10, 170.00),
(8, 3, 40, 47.00), (8, 5, 25, 37.00),
(9, 12, 15, 155.00),
(10, 1, 30, 92.00), (10, 8, 12, 85.00), (10, 6, 18, 92.00);

UPDATE orders o
SET total_amount = COALESCE((
    SELECT SUM(quantity * selling_price) FROM order_items oi WHERE oi.order_id = o.id
), 0);

-- ------------------------------------------------------------
-- shipments (10) -- 5 CUSTOMER_DELIVERY (tied to orders 3,4,5,6,8)
-- and 5 TRANSFER (warehouse-to-warehouse)
-- ------------------------------------------------------------
INSERT INTO shipments (shipment_type, source_warehouse_id, destination_warehouse_id, order_id, carrier_id, tracking_number, status) VALUES
('CUSTOMER_DELIVERY', 1, NULL, 3, 1, 'KE1000123456', 'in_transit'),
('CUSTOMER_DELIVERY', 1, NULL, 4, 3, 'FL2000234567', 'pending'),
('CUSTOMER_DELIVERY', 2, NULL, 5, 4, 'DH3000345678', 'delivered'),
('CUSTOMER_DELIVERY', 3, NULL, 6, 5, 'JT4000456789', 'delivered'),
('CUSTOMER_DELIVERY', 1, NULL, 8, 6, 'NV5000567890', 'in_transit'),
('TRANSFER', 1, 2, NULL, 2, 'TP6000678901', 'delivered'),
('TRANSFER', 1, 3, NULL, 7, 'SC7000789012', 'in_transit'),
('TRANSFER', 2, 4, NULL, 8, 'BE8000890123', 'pending'),
('TRANSFER', 3, 5, NULL, 9, 'AF9000901234', 'delivered'),
('TRANSFER', 1, 4, NULL, 10, 'SP1000012345', 'pending');

-- ------------------------------------------------------------
-- shipment_items (13)
-- ------------------------------------------------------------
INSERT INTO shipment_items (shipment_id, product_id, quantity) VALUES
(1, 2, 12), (1, 6, 20),
(2, 7, 15),
(3, 9, 25), (3, 10, 10),
(4, 11, 20),
(5, 3, 40), (5, 5, 25),
(6, 1, 100),
(7, 5, 80),
(8, 9, 60),
(9, 11, 70),
(10, 4, 30);

-- ------------------------------------------------------------
-- inventory_logs (16) -- ties to inventory rows + performed_by users
-- ------------------------------------------------------------
INSERT INTO inventory_logs (inventory_id, transaction_type, quantity_change, reference_type, reference_id, performed_by, notes) VALUES
(1, 'receive', 500, 'purchase_order', 1, 1, 'Initial stock receipt'),
(2, 'receive', 300, 'purchase_order', 1, 1, 'Initial stock receipt'),
(3, 'receive', 200, 'purchase_order', 2, 2, 'Initial stock receipt'),
(4, 'receive', 150, 'purchase_order', 2, 2, 'Initial stock receipt'),
(5, 'receive', 400, 'purchase_order', 3, 3, 'Initial stock receipt'),
(1, 'shipment_out', -100, 'shipment', 6, 4, 'Transfer to Chiang Mai'),
(3, 'shipment_out', -80, 'shipment', 7, 5, 'Transfer to Pattaya'),
(2, 'shipment_out', -12, 'shipment', 1, 6, 'Customer delivery - Fresh Mart'),
(6, 'shipment_out', -20, 'shipment', 1, 6, 'Customer delivery - Fresh Mart'),
(7, 'shipment_out', -15, 'shipment', 2, 7, 'Customer delivery - Urban Cafe'),
(9, 'shipment_out', -25, 'shipment', 3, 8, 'Customer delivery - Sunny Side Diner'),
(10, 'shipment_out', -10, 'shipment', 3, 8, 'Customer delivery - Sunny Side Diner'),
(11, 'shipment_out', -20, 'shipment', 4, 9, 'Customer delivery - Metro Grocery'),
(3, 'shipment_out', -40, 'shipment', 5, 10, 'Customer delivery - Night Owl Stores'),
(5, 'shipment_out', -25, 'shipment', 5, 10, 'Customer delivery - Night Owl Stores'),
(12, 'shipment_in', 60, 'shipment', 9, 1, 'Received transfer from Pattaya');

-- ------------------------------------------------------------
-- shipment_status_history (18) -- multi-stage history per shipment
-- ------------------------------------------------------------
INSERT INTO shipment_status_history (shipment_id, status, location, notes) VALUES
(1, 'pending', 'Bangkok Central Warehouse', 'Shipment created'),
(1, 'in_transit', 'En route to Fresh Mart', 'Picked up by Kerry Express'),
(2, 'pending', 'Bangkok Central Warehouse', 'Shipment created'),
(3, 'pending', 'Chiang Mai Distribution Center', 'Shipment created'),
(3, 'in_transit', 'En route to Sunny Side Diner', 'Picked up by DHL Thailand'),
(3, 'delivered', 'Sunny Side Diner', 'Delivered and signed for'),
(4, 'pending', 'Pattaya Coastal Warehouse', 'Shipment created'),
(4, 'in_transit', 'En route to Metro Grocery', 'Picked up by J&T Express'),
(4, 'delivered', 'Metro Grocery Co.', 'Delivered and signed for'),
(5, 'pending', 'Bangkok Central Warehouse', 'Shipment created'),
(5, 'in_transit', 'En route to Night Owl Stores', 'Picked up by Ninja Van'),
(6, 'pending', 'Bangkok Central Warehouse', 'Shipment created'),
(6, 'in_transit', 'En route to Chiang Mai', 'Picked up by Thailand Post'),
(6, 'delivered', 'Chiang Mai Distribution Center', 'Received at destination'),
(7, 'pending', 'Bangkok Central Warehouse', 'Shipment created'),
(7, 'in_transit', 'En route to Pattaya', 'Picked up by SCG Express'),
(9, 'delivered', 'Phuket Storage Facility', 'Received at destination'),
(10, 'pending', 'Bangkok Central Warehouse', 'Shipment created');