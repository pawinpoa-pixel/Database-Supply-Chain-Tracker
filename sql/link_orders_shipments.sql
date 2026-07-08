BEGIN;

ALTER TABLE shipments
    ADD COLUMN IF NOT EXISTS shipment_type VARCHAR(20);

UPDATE shipments
SET shipment_type = 'TRANSFER'
WHERE shipment_type IS NULL;

ALTER TABLE shipments
    ALTER COLUMN shipment_type SET NOT NULL;

ALTER TABLE shipments
    ALTER COLUMN destination_warehouse_id DROP NOT NULL;

ALTER TABLE shipments
    ADD COLUMN IF NOT EXISTS order_id INTEGER REFERENCES orders(id);

ALTER TABLE shipments
    ADD CONSTRAINT chk_shipment_type_valid CHECK (shipment_type IN ('TRANSFER', 'CUSTOMER_DELIVERY'));

ALTER TABLE shipments
    ADD CONSTRAINT chk_shipment_target CHECK (
        (shipment_type = 'TRANSFER' AND destination_warehouse_id IS NOT NULL AND order_id IS NULL)
        OR
        (shipment_type = 'CUSTOMER_DELIVERY' AND order_id IS NOT NULL AND destination_warehouse_id IS NULL)
    );

ALTER TABLE shipments
    ADD CONSTRAINT chk_transfer_diff_warehouse CHECK (
        shipment_type <> 'TRANSFER' OR source_warehouse_id <> destination_warehouse_id
    );

COMMIT;