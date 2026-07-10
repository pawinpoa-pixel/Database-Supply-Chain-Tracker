-- 1. New table: order_status_history
-- Mirrors the existing shipment_status_history pattern. Gives you
-- a real audit trail of every order status change, automatically.

CREATE TABLE IF NOT EXISTS order_status_history (
    id                 SERIAL PRIMARY KEY,
    order_id           INTEGER NOT NULL REFERENCES orders(id),
    old_status         VARCHAR(20),
    new_status         VARCHAR(20) NOT NULL,
    changed_at         TIMESTAMPTZ DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION trg_fn_log_order_status_change() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status IS DISTINCT FROM OLD.status THEN
        INSERT INTO order_status_history (order_id, old_status, new_status)
        VALUES (NEW.id, OLD.status, NEW.status);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_order_status_change ON orders;
CREATE TRIGGER trg_order_status_change
AFTER UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION trg_fn_log_order_status_change();


-- ------------------------------------------------------------
-- 2. Defense-in-depth: block negative inventory at the DB level,
-- regardless of which code path (or future bug) tries to do it.
-- ------------------------------------------------------------
CREATE OR REPLACE FUNCTION trg_fn_prevent_negative_inventory() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.quantity_on_hand < 0 THEN
        RAISE EXCEPTION 'Inventory cannot go negative (warehouse %, product %)',
            NEW.warehouse_id, NEW.product_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_no_negative_inventory ON inventory;
CREATE TRIGGER trg_no_negative_inventory
BEFORE UPDATE ON inventory
FOR EACH ROW EXECUTE FUNCTION trg_fn_prevent_negative_inventory();


-- ------------------------------------------------------------
-- 3. Defense-in-depth: mirror the app's "only pending orders can
-- be deleted" rule at the DB level, so it holds even if the API
-- layer has a bug or someone connects directly with a SQL client.
-- ------------------------------------------------------------
CREATE OR REPLACE FUNCTION trg_fn_protect_order_delete() RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status <> 'pending' THEN
        RAISE EXCEPTION 'Cannot delete order % -- status is % (only pending orders can be deleted)',
            OLD.id, OLD.status;
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_protect_order_delete ON orders;
CREATE TRIGGER trg_protect_order_delete
BEFORE DELETE ON orders
FOR EACH ROW EXECUTE FUNCTION trg_fn_protect_order_delete();


-- ------------------------------------------------------------
-- 4. Same idea for shipments -- only pending shipments deletable.
-- ------------------------------------------------------------
CREATE OR REPLACE FUNCTION trg_fn_protect_shipment_delete() RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status <> 'pending' THEN
        RAISE EXCEPTION 'Cannot delete shipment % -- status is % (only pending shipments can be deleted)',
            OLD.id, OLD.status;
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_protect_shipment_delete ON shipments;
CREATE TRIGGER trg_protect_shipment_delete
BEFORE DELETE ON shipments
FOR EACH ROW EXECUTE FUNCTION trg_fn_protect_shipment_delete();