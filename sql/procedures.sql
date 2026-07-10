CREATE OR REPLACE FUNCTION sp_ship_order(
    p_order_id INTEGER,
    p_source_warehouse_id INTEGER,
    p_carrier_id INTEGER DEFAULT NULL,
    p_tracking_number VARCHAR DEFAULT NULL
) RETURNS INTEGER

LANGUAGE plpgsql AS $$
DECLARE
    v_order_status VARCHAR(20);
    v_shipment_id  INTEGER;
    
BEGIN
    SELECT status INTO v_order_status FROM orders WHERE id = p_order_id;

    IF v_order_status IS NULL THEN
        RAISE EXCEPTION 'Order % not found', p_order_id;
    END IF;

    IF v_order_status <> 'pending' THEN
        RAISE EXCEPTION 'Order % is not pending', p_order_id;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM order_items WHERE order_id = p_order_id) THEN
        RAISE EXCEPTION 'Order % has no items', p_order_id;
    END IF;

    IF EXISTS (
        SELECT 1
        FROM order_items oi
        LEFT JOIN inventory inv
            ON inv.product_id = oi.product_id AND inv.warehouse_id = p_source_warehouse_id
        WHERE oi.order_id = p_order_id
          AND COALESCE(inv.quantity_on_hand, 0) < oi.quantity
    ) THEN
        RAISE EXCEPTION 'Not enough stock at warehouse % for order %', p_source_warehouse_id, p_order_id;
    END IF;

    INSERT INTO shipments (shipment_type, source_warehouse_id, order_id, carrier_id, tracking_number, status)
    VALUES ('CUSTOMER_DELIVERY', p_source_warehouse_id, p_order_id, p_carrier_id, p_tracking_number, 'pending')
    RETURNING id INTO v_shipment_id;

    INSERT INTO shipment_items (shipment_id, product_id, quantity)
    SELECT v_shipment_id, product_id, quantity
    FROM order_items
    WHERE order_id = p_order_id;

    INSERT INTO shipment_status_history (shipment_id, status)
    VALUES (v_shipment_id, 'pending');

    UPDATE orders SET status = 'processing' WHERE id = p_order_id;

    RETURN v_shipment_id;
END;
$$;

-- Receives a purchase order into a warehouse: upserts inventory,
-- logs each receipt, and marks the PO as received.

CREATE OR REPLACE FUNCTION sp_receive_purchase_order(
    p_po_id INTEGER,
    p_warehouse_id INTEGER,
    p_performed_by INTEGER
) RETURNS VOID
LANGUAGE plpgsql AS $$
DECLARE
    v_po_status VARCHAR(20);
    r_item      RECORD;
    v_inv_id    INTEGER;
BEGIN
    SELECT status INTO v_po_status FROM purchase_orders WHERE id = p_po_id;

    IF v_po_status IS NULL THEN
        RAISE EXCEPTION 'Purchase order % not found', p_po_id;
    END IF;

    IF v_po_status = 'received' THEN
        RAISE EXCEPTION 'Purchase order % has already been received', p_po_id;
    END IF;

    FOR r_item IN
        SELECT product_id, quantity FROM purchase_order_items WHERE po_id = p_po_id
    LOOP
        SELECT id INTO v_inv_id
        FROM inventory
        WHERE warehouse_id = p_warehouse_id AND product_id = r_item.product_id;

        IF v_inv_id IS NULL THEN
            INSERT INTO inventory (warehouse_id, product_id, quantity_on_hand)
            VALUES (p_warehouse_id, r_item.product_id, r_item.quantity)
            RETURNING id INTO v_inv_id;
        ELSE
            UPDATE inventory
            SET quantity_on_hand = quantity_on_hand + r_item.quantity,
                last_updated = NOW()
            WHERE id = v_inv_id;
        END IF;

        INSERT INTO inventory_logs (inventory_id, transaction_type, quantity_change, reference_type, reference_id, performed_by, notes)
        VALUES (v_inv_id, 'receive', r_item.quantity, 'purchase_order', p_po_id, p_performed_by, 'Received via sp_receive_purchase_order');
    END LOOP;

    UPDATE purchase_orders SET status = 'received' WHERE id = p_po_id;
END;
$$;
