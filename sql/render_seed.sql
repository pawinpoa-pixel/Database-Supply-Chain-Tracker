-- Demo dataset for a fresh Render PostgreSQL database.
-- Compatible with migration 0003_multi_tenant_scoping.sql.
-- All master data belongs to demo user id 1.
-- Application login password for every seeded user: Password123!

CREATE EXTENSION IF NOT EXISTS pgcrypto;

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
    customers,
    carriers,
    warehouses,
    suppliers,
    categories,
    users
RESTART IDENTITY CASCADE;

INSERT INTO users (username, email, password) VALUES
('admin_som',   'som.admin@supplychain.co.th',   crypt('Password123!', gen_salt('bf'))),
('jaidee_w',    'jaidee.w@supplychain.co.th',    crypt('Password123!', gen_salt('bf'))),
('anong_p',     'anong.p@supplychain.co.th',     crypt('Password123!', gen_salt('bf'))),
('kittipong_s', 'kittipong.s@supplychain.co.th', crypt('Password123!', gen_salt('bf'))),
('malee_t',     'malee.t@supplychain.co.th',     crypt('Password123!', gen_salt('bf'))),
('preecha_n',   'preecha.n@supplychain.co.th',   crypt('Password123!', gen_salt('bf'))),
('supaporn_k',  'supaporn.k@supplychain.co.th',  crypt('Password123!', gen_salt('bf'))),
('wichai_r',    'wichai.r@supplychain.co.th',    crypt('Password123!', gen_salt('bf'))),
('nattaya_c',   'nattaya.c@supplychain.co.th',   crypt('Password123!', gen_salt('bf'))),
('somchai_b',   'somchai.b@supplychain.co.th',   crypt('Password123!', gen_salt('bf')));

INSERT INTO categories
(category_name, description, parent_category_id, color_hex, user_id) VALUES
('Beverages',         'Soft drinks, tea and water',            NULL, '#2563eb', 1),
('Dairy',             'Milk, cheese and dairy products',       NULL, '#0ea5e9', 1),
('Snacks',            'Chips, nuts and packaged snacks',       NULL, '#f59e0b', 1),
('Frozen Foods',      'Frozen meals and ingredients',          NULL, '#06b6d4', 1),
('Bakery',            'Bread, pastries and baked goods',       NULL, '#d97706', 1),
('Produce',           'Fresh fruit and vegetables',            NULL, '#16a34a', 1),
('Meat and Poultry',  'Fresh and packaged meat products',      NULL, '#dc2626', 1),
('Cleaning Supplies', 'Commercial cleaning products',          NULL, '#7c3aed', 1),
('Personal Care',     'Hygiene and personal-care products',    NULL, '#db2777', 1),
('Canned Goods',      'Canned and preserved foods',            NULL, '#64748b', 1);

INSERT INTO suppliers
(company_name, contact_name, email, phone, address, user_id) VALUES
('Golden Valley Beverages Co.', 'Somchai Boonmee',   'sales@goldenvalley.example', '02-555-0101', '88 Sukhumvit Road, Bangkok', 1),
('Sunrise Dairy Farms',         'Malee Thongchai',   'contact@sunrisedairy.example','02-555-0102', '12 Ratchada Road, Bangkok', 1),
('Crunch Time Snacks Ltd.',     'Wichai Ruangsri',   'orders@crunchtime.example',  '02-555-0103', '45 Silom Road, Bangkok', 1),
('Arctic Fresh Frozen Foods',   'Nattaya Chaiyaporn','info@arcticfresh.example',   '02-555-0104', '77 Rama IV Road, Bangkok', 1),
('Golden Crust Bakery Supply',  'Preecha Nualsri',   'sales@goldencrust.example',  '02-555-0105', '23 Phahonyothin Road, Bangkok', 1),
('Green Acres Produce',         'Anong Petchara',    'contact@greenacres.example', '02-555-0106', '56 Ladprao Road, Bangkok', 1),
('Premium Meats Wholesale',     'Kittipong Saelim',  'orders@premiummeats.example','02-555-0107', '34 Bang Na Road, Bangkok', 1),
('SparkleClean Supplies Co.',   'Supaporn Kraisri',  'sales@sparkleclean.example','02-555-0108', '19 Charoen Krung Road, Bangkok', 1),
('PureCare Personal Products',  'Jaidee Wattana',    'info@purecare.example',      '02-555-0109', '61 Sathorn Road, Bangkok', 1),
('Harvest Best Canned Goods',   'Somsak Uraiwan',    'contact@harvestbest.example','02-555-0110','8 Petchaburi Road, Bangkok', 1);

INSERT INTO warehouses
(warehouse_name, address, capacity, user_id) VALUES
('Bangkok Central Warehouse',       '100 Bang Phlat, Bangkok',        50000, 1),
('Chiang Mai Distribution Center',  '25 Hang Dong Road, Chiang Mai', 30000, 1),
('Pattaya Coastal Warehouse',       '14 Sukhumvit Road, Pattaya',    20000, 1),
('Khon Kaen Regional Hub',          '9 Mittraphap Road, Khon Kaen',  25000, 1),
('Phuket Storage Facility',         '33 Chalermprakiat Road, Phuket',15000, 1),
('Nonthaburi Cold Storage',         '77 Rattanathibet, Nonthaburi',  18000, 1),
('Rayong Logistics Center',         '5 Sukhumvit Road, Rayong',      22000, 1),
('Udon Thani Warehouse',            '41 Prajak Road, Udon Thani',    17000, 1),
('Hat Yai Southern Hub',            '62 Niphat Uthit Road, Hat Yai', 19000, 1),
('Ayutthaya Overflow Storage',      '3 Rojana Road, Ayutthaya',      12000, 1);

INSERT INTO carriers
(carrier_name, phone, email, user_id) VALUES
('Kerry Express',       '02-800-4000', 'support@kerry.example',       1),
('Thailand Post',       '1545',        'contact@thaipost.example',    1),
('Flash Express',       '1425',        'support@flash.example',       1),
('DHL Thailand',        '02-345-5000', 'thailand@dhl.example',       1),
('J&T Express',         '02-460-5988', 'support@jt.example',         1),
('Ninja Van Thailand',  '02-006-9696', 'support@ninjavan.example',   1),
('SCG Express',         '02-586-3333', 'contact@scgexpress.example', 1),
('Best Express',        '02-116-8999', 'support@best.example',       1),
('Alpha Fast Logistics','02-222-3344', 'info@alphafast.example',     1),
('Speedy Cargo Co.',    '02-333-4455', 'contact@speedycargo.example',1);

INSERT INTO customers
(customer_name, email, phone, address, user_id) VALUES
('Golden Spoon Restaurant Group', 'purchasing@goldenspoon.example','02-700-1001','10 Thonglor Road, Bangkok', 1),
('QuickBite Convenience Stores',  'orders@quickbite.example',      '02-700-1002','22 Ari Road, Bangkok', 1),
('Fresh Mart Supermarket',        'supply@freshmart.example',      '02-700-1003','5 Ekkamai Road, Bangkok', 1),
('Urban Cafe Chain',              'purchasing@urbancafe.example',  '02-700-1004','18 Sathorn Road, Bangkok', 1),
('Sunny Side Diner',              'orders@sunnyside.example',      '02-700-1005','7 Phrom Phong Road, Bangkok', 1),
('Metro Grocery Co.',             'supply@metrogrocery.example',   '02-700-1006','33 Bangna Road, Bangkok', 1),
('Green Leaf Restaurants',        'purchasing@greenleaf.example',  '02-700-1007','15 Ratchada Road, Bangkok', 1),
('Night Owl 24hr Stores',         'orders@nightowl.example',       '02-700-1008','9 Silom Road, Bangkok', 1),
('Coastal Kitchen Group',         'purchasing@coastalkitchen.example','038-700-1009','20 Beach Road, Pattaya', 1),
('Big Basket Wholesale Club',     'supply@bigbasket.example',      '02-700-1010','44 Ladprao Road, Bangkok', 1);

INSERT INTO products
(sku, product_name, category_id, unit_price, reorder_level, is_active, user_id) VALUES
('BEV-001','Thai Iced Tea Concentrate 1L',1,89.00,50,TRUE,1),
('BEV-002','Sparkling Water 500ml Case',1,240.00,30,TRUE,1),
('DAI-001','Fresh Milk 1L',2,45.00,80,TRUE,1),
('DAI-002','Cheddar Cheese Block 500g',2,165.00,40,TRUE,1),
('SNK-001','Potato Chips 150g',3,35.00,100,TRUE,1),
('SNK-002','Mixed Nuts 200g',3,89.00,60,TRUE,1),
('FRZ-001','Frozen Chicken Nuggets 1kg',4,129.00,50,TRUE,1),
('FRZ-002','Frozen Mixed Vegetables 1kg',4,79.00,45,TRUE,1),
('BAK-001','White Sandwich Bread',5,32.00,70,TRUE,1),
('BAK-002','Croissants Six Pack',5,99.00,40,TRUE,1),
('PRD-001','Fresh Tomatoes 1kg',6,55.00,60,TRUE,1),
('MEA-001','Chicken Breast 1kg',7,149.00,50,TRUE,1);

INSERT INTO inventory (warehouse_id, product_id, quantity_on_hand) VALUES
(1,1,500),(1,2,300),(1,3,200),(1,4,150),(1,5,400),(1,6,180),
(2,1,250),(2,3,180),(2,7,90),(2,8,120),
(3,2,310),(3,5,275),(3,9,160),(3,10,100),
(4,11,140),(4,12,95);

INSERT INTO purchase_orders
(supplier_id, order_date, expected_delivery_date, status) VALUES
(1,NOW()-INTERVAL '20 days',CURRENT_DATE-10,'received'),
(2,NOW()-INTERVAL '18 days',CURRENT_DATE-8,'received'),
(3,NOW()-INTERVAL '15 days',CURRENT_DATE+2,'pending'),
(4,NOW()-INTERVAL '14 days',CURRENT_DATE+4,'pending'),
(5,NOW()-INTERVAL '12 days',CURRENT_DATE-5,'received'),
(6,NOW()-INTERVAL '10 days',CURRENT_DATE+6,'pending'),
(7,NOW()-INTERVAL '9 days', CURRENT_DATE-1,'received'),
(8,NOW()-INTERVAL '8 days', CURRENT_DATE+9,'pending'),
(9,NOW()-INTERVAL '7 days', CURRENT_DATE+3,'pending'),
(10,NOW()-INTERVAL '5 days',CURRENT_DATE+5,'pending');

INSERT INTO purchase_order_items (po_id, product_id, quantity, unit_cost) VALUES
(1,1,200,60.00),(1,2,100,180.00),(2,3,300,30.00),(2,4,100,120.00),
(3,5,400,20.00),(4,7,200,90.00),(4,8,150,55.00),(5,9,300,20.00),
(5,10,150,65.00),(6,11,250,35.00),(7,12,200,100.00),(7,1,100,58.00),
(8,6,180,60.00),(9,2,90,175.00),(10,4,60,118.00);

INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES
(1,NOW()-INTERVAL '10 days','pending',0),
(2,NOW()-INTERVAL '9 days','pending',0),
(3,NOW()-INTERVAL '8 days','processing',0),
(4,NOW()-INTERVAL '7 days','processing',0),
(5,NOW()-INTERVAL '6 days','fulfilled',0),
(6,NOW()-INTERVAL '5 days','fulfilled',0),
(7,NOW()-INTERVAL '4 days','pending',0),
(8,NOW()-INTERVAL '3 days','processing',0),
(9,NOW()-INTERVAL '2 days','pending',0),
(10,NOW()-INTERVAL '1 day','fulfilled',0);

INSERT INTO order_items (order_id, product_id, quantity, selling_price) VALUES
(1,1,24,95.00),(1,5,40,38.00),(2,3,30,48.00),(3,2,12,250.00),
(3,6,20,95.00),(4,7,15,135.00),(5,9,25,35.00),(5,10,10,105.00),
(6,11,20,60.00),(7,4,10,170.00),(8,3,40,47.00),(8,5,25,37.00),
(9,12,15,155.00),(10,1,30,92.00),(10,8,12,85.00),(10,6,18,92.00);

UPDATE orders AS o
SET total_amount = (
    SELECT COALESCE(SUM(oi.quantity * oi.selling_price), 0)
    FROM order_items AS oi
    WHERE oi.order_id = o.id
);

INSERT INTO shipments
(shipment_type, shipment_date, source_warehouse_id, destination_warehouse_id,
 order_id, carrier_id, tracking_number, status) VALUES
('CUSTOMER_DELIVERY',NOW()-INTERVAL '7 days',1,NULL,3,1,'KE1000123456','in_transit'),
('CUSTOMER_DELIVERY',NOW()-INTERVAL '6 days',1,NULL,4,3,'FL2000234567','pending'),
('CUSTOMER_DELIVERY',NOW()-INTERVAL '5 days',2,NULL,5,4,'DH3000345678','delivered'),
('CUSTOMER_DELIVERY',NOW()-INTERVAL '4 days',3,NULL,6,5,'JT4000456789','delivered'),
('CUSTOMER_DELIVERY',NOW()-INTERVAL '3 days',1,NULL,8,6,'NV5000567890','in_transit'),
('TRANSFER',NOW()-INTERVAL '9 days',1,2,NULL,2,'TP6000678901','delivered'),
('TRANSFER',NOW()-INTERVAL '8 days',1,3,NULL,7,'SC7000789012','in_transit'),
('TRANSFER',NOW()-INTERVAL '7 days',2,4,NULL,8,'BE8000890123','pending'),
('TRANSFER',NOW()-INTERVAL '6 days',3,4,NULL,9,'AF9000901234','delivered'),
('TRANSFER',NOW()-INTERVAL '5 days',1,4,NULL,10,'SP1000012345','pending');

INSERT INTO shipment_items (shipment_id, product_id, quantity) VALUES
(1,2,12),(1,6,20),(2,7,15),(3,9,25),(3,10,10),(4,11,20),
(5,3,40),(5,5,25),(6,1,100),(7,5,80),(8,9,60),(9,11,70),(10,4,30);

INSERT INTO inventory_logs
(inventory_id, transaction_type, quantity_change, reference_type, reference_id,
 performed_by, log_timestamp, notes) VALUES
(1,'receive',500,'purchase_order',1,1,NOW()-INTERVAL '20 days','Initial receipt'),
(2,'receive',300,'purchase_order',1,1,NOW()-INTERVAL '20 days','Initial receipt'),
(3,'receive',200,'purchase_order',2,2,NOW()-INTERVAL '18 days','Initial receipt'),
(4,'receive',150,'purchase_order',2,2,NOW()-INTERVAL '18 days','Initial receipt'),
(5,'receive',400,'purchase_order',3,3,NOW()-INTERVAL '15 days','Initial receipt'),
(1,'shipment_out',-100,'shipment',6,4,NOW()-INTERVAL '9 days','Transfer to Chiang Mai'),
(3,'shipment_out',-80,'shipment',7,5,NOW()-INTERVAL '8 days','Transfer to Pattaya'),
(2,'shipment_out',-12,'shipment',1,6,NOW()-INTERVAL '7 days','Customer delivery'),
(6,'shipment_out',-20,'shipment',1,6,NOW()-INTERVAL '7 days','Customer delivery'),
(9,'shipment_out',-15,'shipment',2,7,NOW()-INTERVAL '6 days','Customer delivery'),
(13,'shipment_out',-25,'shipment',3,8,NOW()-INTERVAL '5 days','Customer delivery'),
(14,'shipment_out',-10,'shipment',3,8,NOW()-INTERVAL '5 days','Customer delivery'),
(15,'shipment_out',-20,'shipment',4,9,NOW()-INTERVAL '4 days','Customer delivery'),
(3,'shipment_out',-40,'shipment',5,10,NOW()-INTERVAL '3 days','Customer delivery'),
(5,'shipment_out',-25,'shipment',5,10,NOW()-INTERVAL '3 days','Customer delivery'),
(16,'shipment_in',60,'shipment',9,1,NOW()-INTERVAL '5 days','Received warehouse transfer');

INSERT INTO shipment_status_history
(shipment_id, status, location, status_timestamp, notes) VALUES
(1,'pending','Bangkok Central Warehouse',NOW()-INTERVAL '7 days','Shipment created'),
(1,'in_transit','Bangkok',NOW()-INTERVAL '6 days','Collected by carrier'),
(2,'pending','Bangkok Central Warehouse',NOW()-INTERVAL '6 days','Shipment created'),
(3,'pending','Chiang Mai Distribution Center',NOW()-INTERVAL '5 days','Shipment created'),
(3,'in_transit','Chiang Mai',NOW()-INTERVAL '4 days','Collected by carrier'),
(3,'delivered','Sunny Side Diner',NOW()-INTERVAL '3 days','Signed delivery'),
(4,'pending','Pattaya Coastal Warehouse',NOW()-INTERVAL '4 days','Shipment created'),
(4,'in_transit','Pattaya',NOW()-INTERVAL '3 days','Collected by carrier'),
(4,'delivered','Metro Grocery Co.',NOW()-INTERVAL '2 days','Signed delivery'),
(5,'pending','Bangkok Central Warehouse',NOW()-INTERVAL '3 days','Shipment created'),
(5,'in_transit','Bangkok',NOW()-INTERVAL '2 days','Collected by carrier'),
(6,'pending','Bangkok Central Warehouse',NOW()-INTERVAL '9 days','Transfer created'),
(6,'in_transit','Highway 1',NOW()-INTERVAL '8 days','Transfer departed'),
(6,'delivered','Chiang Mai Distribution Center',NOW()-INTERVAL '7 days','Transfer received'),
(7,'pending','Bangkok Central Warehouse',NOW()-INTERVAL '8 days','Transfer created'),
(7,'in_transit','Chonburi',NOW()-INTERVAL '7 days','Transfer departed'),
(9,'delivered','Khon Kaen Regional Hub',NOW()-INTERVAL '5 days','Transfer received'),
(10,'pending','Bangkok Central Warehouse',NOW()-INTERVAL '5 days','Transfer created');
