-- Recurring orders billed on a separate cadence from delivery
-- (e.g. deliver milk weekly, bill monthly).
--
-- Subscriptions auto-generate real rows in the existing orders/
-- order_items tables (tagged via orders.subscription_id) so they flow
-- through the exact same fulfillment/shipping path as any one-off
-- order. Invoices then aggregate whichever of those orders haven't
-- been billed yet (orders.invoice_id IS NULL) into one bill -- that's
-- the piece that decouples billing cadence from delivery cadence.

CREATE TABLE IF NOT EXISTS subscriptions (
    id                        SERIAL PRIMARY KEY,
    user_id                   INTEGER NOT NULL REFERENCES users(id),
    customer_id               INTEGER NOT NULL REFERENCES customers(id),
    status                    VARCHAR(20) NOT NULL DEFAULT 'active',
    delivery_frequency_days   INTEGER NOT NULL,
    billing_frequency_days    INTEGER NOT NULL,
    start_date                DATE NOT NULL,
    next_delivery_date        DATE NOT NULL,
    next_billing_date         DATE NOT NULL,
    created_at                TIMESTAMPTZ DEFAULT NOW(),
    CHECK (status IN ('active', 'paused', 'cancelled'))
);

CREATE TABLE IF NOT EXISTS invoices (
    id                     SERIAL PRIMARY KEY,
    user_id                INTEGER NOT NULL REFERENCES users(id),
    subscription_id        INTEGER NOT NULL REFERENCES subscriptions(id),
    billing_period_start   DATE NOT NULL,
    billing_period_end     DATE NOT NULL,
    issue_date             DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date               DATE NOT NULL,
    status                 VARCHAR(20) NOT NULL DEFAULT 'pending',
    total_amount           NUMERIC(10, 2) NOT NULL DEFAULT 0,
    paid_at                TIMESTAMPTZ,
    CHECK (status IN ('pending', 'paid', 'overdue', 'cancelled'))
);

CREATE TABLE IF NOT EXISTS subscription_items (
    id                      SERIAL PRIMARY KEY,
    subscription_id         INTEGER NOT NULL REFERENCES subscriptions(id),
    product_id              INTEGER NOT NULL REFERENCES products(id),
    quantity_per_delivery   INTEGER NOT NULL,
    unit_price              NUMERIC(10, 2) NOT NULL
);

ALTER TABLE orders ADD COLUMN IF NOT EXISTS subscription_id INTEGER REFERENCES subscriptions(id);
ALTER TABLE orders ADD COLUMN IF NOT EXISTS invoice_id INTEGER REFERENCES invoices(id);

CREATE INDEX IF NOT EXISTS idx_orders_subscription_id ON orders(subscription_id);
CREATE INDEX IF NOT EXISTS idx_orders_invoice_id ON orders(invoice_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_customer_id ON subscriptions(customer_id);
CREATE INDEX IF NOT EXISTS idx_subscription_items_subscription_id ON subscription_items(subscription_id);
CREATE INDEX IF NOT EXISTS idx_invoices_subscription_id ON invoices(subscription_id);
