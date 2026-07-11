-- Every user was sharing one global pool of categories, suppliers,
-- warehouses, carriers, customers and products -- there was no owner
-- column anywhere, so any logged-in user could see and edit everyone
-- else's data. This adds a user_id column to the six "master" tables
-- and scopes everything else (inventory, purchase orders, orders,
-- shipments, logs) transitively through them.
--
-- Existing rows predate this column, so they're backfilled to the
-- oldest account (MIN(id) from users) rather than deleted -- there's
-- no way to know who "really" owned them, and this is demo/test data
-- from before per-user isolation existed.

ALTER TABLE categories ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);
ALTER TABLE suppliers  ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);
ALTER TABLE warehouses ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);
ALTER TABLE carriers   ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);
ALTER TABLE customers  ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);
ALTER TABLE products   ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);

UPDATE categories SET user_id = (SELECT MIN(id) FROM users) WHERE user_id IS NULL;
UPDATE suppliers  SET user_id = (SELECT MIN(id) FROM users) WHERE user_id IS NULL;
UPDATE warehouses SET user_id = (SELECT MIN(id) FROM users) WHERE user_id IS NULL;
UPDATE carriers   SET user_id = (SELECT MIN(id) FROM users) WHERE user_id IS NULL;
UPDATE customers  SET user_id = (SELECT MIN(id) FROM users) WHERE user_id IS NULL;
UPDATE products   SET user_id = (SELECT MIN(id) FROM users) WHERE user_id IS NULL;

ALTER TABLE categories ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE suppliers  ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE warehouses ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE carriers   ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE customers  ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE products   ALTER COLUMN user_id SET NOT NULL;

-- SKU/barcode uniqueness moves from global to per-user, so two users
-- can each use SKU "ABC123" without colliding. The original columns
-- were declared unique=True (sku also had index=True), which SQLAlchemy
-- backs with plain unique indexes rather than named table constraints,
-- so both the index and constraint forms are dropped here.
DROP INDEX IF EXISTS ix_products_sku;
DROP INDEX IF EXISTS ix_products_barcode;
ALTER TABLE products DROP CONSTRAINT IF EXISTS products_sku_key;
ALTER TABLE products DROP CONSTRAINT IF EXISTS products_barcode_key;
ALTER TABLE products ADD CONSTRAINT uq_products_user_sku UNIQUE (user_id, sku);
ALTER TABLE products ADD CONSTRAINT uq_products_user_barcode UNIQUE (user_id, barcode);
