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