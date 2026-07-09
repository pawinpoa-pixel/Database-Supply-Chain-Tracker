-- Adds richer catalog fields to categories/products.
-- Base.metadata.create_all() only creates missing tables, not new columns
-- on tables that already exist, so this has to be applied by hand against
-- the running database (see README for how to connect).

ALTER TABLE categories
    ADD COLUMN IF NOT EXISTS parent_category_id INTEGER REFERENCES categories(id),
    ADD COLUMN IF NOT EXISTS color_hex VARCHAR(7) DEFAULT '#4361ee';

ALTER TABLE products
    ADD COLUMN IF NOT EXISTS brand VARCHAR(100),
    ADD COLUMN IF NOT EXISTS barcode VARCHAR(64) UNIQUE,
    ADD COLUMN IF NOT EXISTS description TEXT,
    ADD COLUMN IF NOT EXISTS unit_of_measure VARCHAR(20) DEFAULT 'EA',
    ADD COLUMN IF NOT EXISTS weight_kg NUMERIC(10, 3),
    ADD COLUMN IF NOT EXISTS primary_supplier_id INTEGER REFERENCES suppliers(id),
    ADD COLUMN IF NOT EXISTS max_stock_level INTEGER,
    ADD COLUMN IF NOT EXISTS lead_time_days INTEGER,
    ADD COLUMN IF NOT EXISTS image_url VARCHAR(500),
    ADD COLUMN IF NOT EXISTS tags VARCHAR(255);
