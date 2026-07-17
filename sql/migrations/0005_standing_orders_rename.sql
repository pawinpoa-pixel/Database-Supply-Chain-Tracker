-- Reframes 0004's "subscriptions" concept as a "standing order" --
-- the standard procurement/ERP term for a customer's standing
-- arrangement for periodic deliveries against one agreement (also
-- called a blanket order), rather than a consumer subscription.
--
-- Also gives invoices an explicit who (customer_id, direct rather than
-- via a join through the standing order) and what (a new invoice_items
-- table, itemized by product) instead of only an aggregate total tied
-- to opaque order references.
--
-- main.py runs Base.metadata.create_all() before run_migrations(), so
-- by the time this file runs, SQLAlchemy may have already created
-- empty standing_orders/standing_order_items tables from the current
-- (renamed) models -- these DO blocks only attempt the rename if the
-- old table/column is still there, dropping the empty auto-created
-- shell first so the rename can take its place. On a fresh database
-- (no "subscriptions" table ever existed), everything here is a no-op
-- and create_all already produced the right end state.

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'subscriptions') THEN
        DROP TABLE IF EXISTS standing_order_items CASCADE;
        DROP TABLE IF EXISTS standing_orders CASCADE;
        ALTER TABLE subscriptions RENAME TO standing_orders;
        ALTER TABLE subscription_items RENAME TO standing_order_items;
        ALTER TABLE standing_order_items RENAME COLUMN subscription_id TO standing_order_id;
    END IF;
END $$;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'invoices' AND column_name = 'subscription_id'
    ) THEN
        ALTER TABLE invoices RENAME COLUMN subscription_id TO standing_order_id;
    END IF;
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'orders' AND column_name = 'subscription_id'
    ) THEN
        ALTER TABLE orders RENAME COLUMN subscription_id TO standing_order_id;
    END IF;
END $$;

ALTER TABLE invoices ADD COLUMN IF NOT EXISTS customer_id INTEGER REFERENCES customers(id);
UPDATE invoices i
SET customer_id = so.customer_id
FROM standing_orders so
WHERE so.id = i.standing_order_id AND i.customer_id IS NULL;
ALTER TABLE invoices ALTER COLUMN customer_id SET NOT NULL;

CREATE TABLE IF NOT EXISTS invoice_items (
    id          SERIAL PRIMARY KEY,
    invoice_id  INTEGER NOT NULL REFERENCES invoices(id),
    product_id  INTEGER NOT NULL REFERENCES products(id),
    quantity    INTEGER NOT NULL,
    unit_price  NUMERIC(10, 2) NOT NULL
);

-- Backfill itemized lines for any invoice generated before invoice_items
-- existed, from the order_items of whatever orders it already covers.
DO $$
DECLARE
    inv RECORD;
    agg RECORD;
BEGIN
    FOR inv IN SELECT id FROM invoices LOOP
        IF NOT EXISTS (SELECT 1 FROM invoice_items WHERE invoice_id = inv.id) THEN
            FOR agg IN
                SELECT oi.product_id, SUM(oi.quantity) AS quantity, oi.selling_price AS unit_price
                FROM orders o
                JOIN order_items oi ON oi.order_id = o.id
                WHERE o.invoice_id = inv.id
                GROUP BY oi.product_id, oi.selling_price
            LOOP
                INSERT INTO invoice_items (invoice_id, product_id, quantity, unit_price)
                VALUES (inv.id, agg.product_id, agg.quantity, agg.unit_price);
            END LOOP;
        END IF;
    END LOOP;
END $$;

DROP INDEX IF EXISTS idx_orders_subscription_id;
DROP INDEX IF EXISTS idx_subscriptions_customer_id;
DROP INDEX IF EXISTS idx_subscription_items_subscription_id;
DROP INDEX IF EXISTS idx_invoices_subscription_id;

CREATE INDEX IF NOT EXISTS idx_orders_standing_order_id ON orders(standing_order_id);
CREATE INDEX IF NOT EXISTS idx_standing_orders_customer_id ON standing_orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_standing_order_items_standing_order_id ON standing_order_items(standing_order_id);
CREATE INDEX IF NOT EXISTS idx_invoices_standing_order_id ON invoices(standing_order_id);
CREATE INDEX IF NOT EXISTS idx_invoices_customer_id ON invoices(customer_id);
CREATE INDEX IF NOT EXISTS idx_invoice_items_invoice_id ON invoice_items(invoice_id);
