CREATE TABLE IF NOT EXISTS users (
    id        SERIAL PRIMARY KEY,
    username  VARCHAR(50)  UNIQUE NOT NULL,
    email     VARCHAR(100) UNIQUE NOT NULL,
    password  TEXT         NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS categories (
    id            SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description   TEXT
);

CREATE TABLE IF NOT EXISTS suppliers (
    id           SERIAL PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    contact_name VARCHAR(100),
    email        VARCHAR(100),
    phone        VARCHAR(30),
    address      TEXT
);

CREATE TABLE IF NOT EXISTS warehouses (
    id             SERIAL PRIMARY KEY,
    warehouse_name VARCHAR(150) NOT NULL,
    address        TEXT,
    capacity       INTEGER
);

CREATE TABLE IF NOT EXISTS carriers (
    id           SERIAL PRIMARY KEY,
    carrier_name VARCHAR(150) NOT NULL,
    phone        VARCHAR(30),
    email        VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS customers (
    id            SERIAL PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    email         VARCHAR(100),
    phone         VARCHAR(30),
    address       TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id             SERIAL PRIMARY KEY,
    sku            VARCHAR(50) UNIQUE NOT NULL,
    product_name   VARCHAR(150) NOT NULL,
    category_id    INTEGER REFERENCES categories(id),
    unit_price     NUMERIC(10, 2) NOT NULL DEFAULT 0,
    reorder_level  INTEGER NOT NULL DEFAULT 0,
    is_active      BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS inventory (
    id                SERIAL PRIMARY KEY,
    warehouse_id      INTEGER NOT NULL REFERENCES warehouses(id),
    product_id        INTEGER NOT NULL REFERENCES products(id),
    quantity_on_hand  INTEGER NOT NULL DEFAULT 0,
    last_updated      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (warehouse_id, product_id)
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    id                       SERIAL PRIMARY KEY,
    supplier_id              INTEGER NOT NULL REFERENCES suppliers(id),
    order_date               TIMESTAMPTZ DEFAULT NOW(),
    expected_delivery_date   DATE,
    status                   VARCHAR(20) NOT NULL DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS purchase_order_items (
    id          SERIAL PRIMARY KEY,
    po_id       INTEGER NOT NULL REFERENCES purchase_orders(id),
    product_id  INTEGER NOT NULL REFERENCES products(id),
    quantity    INTEGER NOT NULL,
    unit_cost   NUMERIC(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id            SERIAL PRIMARY KEY,
    customer_id   INTEGER NOT NULL REFERENCES customers(id),
    order_date    TIMESTAMPTZ DEFAULT NOW(),
    status        VARCHAR(20) NOT NULL DEFAULT 'pending',
    total_amount  NUMERIC(10, 2) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS order_items (
    id             SERIAL PRIMARY KEY,
    order_id       INTEGER NOT NULL REFERENCES orders(id),
    product_id     INTEGER NOT NULL REFERENCES products(id),
    quantity       INTEGER NOT NULL,
    selling_price  NUMERIC(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS shipments (
    id                          SERIAL PRIMARY KEY,
    shipment_type               VARCHAR(20) NOT NULL,
    shipment_date               TIMESTAMPTZ DEFAULT NOW(),
    source_warehouse_id         INTEGER NOT NULL REFERENCES warehouses(id),
    destination_warehouse_id    INTEGER REFERENCES warehouses(id),
    order_id                    INTEGER REFERENCES orders(id),
    carrier_id                  INTEGER REFERENCES carriers(id),
    tracking_number             VARCHAR(100),
    status                      VARCHAR(20) NOT NULL DEFAULT 'pending',
    CHECK (shipment_type IN ('TRANSFER', 'CUSTOMER_DELIVERY')),
    CHECK (
        (shipment_type = 'TRANSFER' AND destination_warehouse_id IS NOT NULL AND order_id IS NULL)
        OR
        (shipment_type = 'CUSTOMER_DELIVERY' AND order_id IS NOT NULL AND destination_warehouse_id IS NULL)
    ),
    CHECK (shipment_type <> 'TRANSFER' OR source_warehouse_id <> destination_warehouse_id)
);

CREATE TABLE IF NOT EXISTS shipment_items (
    id            SERIAL PRIMARY KEY,
    shipment_id   INTEGER NOT NULL REFERENCES shipments(id),
    product_id    INTEGER NOT NULL REFERENCES products(id),
    quantity      INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory_logs (
    id                SERIAL PRIMARY KEY,
    inventory_id      INTEGER NOT NULL REFERENCES inventory(id),
    transaction_type  VARCHAR(30) NOT NULL,
    quantity_change   INTEGER NOT NULL,
    reference_type    VARCHAR(30),
    reference_id      INTEGER,
    performed_by      INTEGER REFERENCES users(id),
    log_timestamp     TIMESTAMPTZ DEFAULT NOW(),
    notes             TEXT
);

CREATE TABLE IF NOT EXISTS shipment_status_history (
    id                 SERIAL PRIMARY KEY,
    shipment_id        INTEGER NOT NULL REFERENCES shipments(id),
    status             VARCHAR(20) NOT NULL,
    location           VARCHAR(150),
    status_timestamp   TIMESTAMPTZ DEFAULT NOW(),
    notes              TEXT
);
