-- Drops the tags and lead_time_days columns added in 0001 — decided
-- against for a project this size. Only the demo product row created
-- during testing had data in these columns.

ALTER TABLE products
    DROP COLUMN IF EXISTS tags,
    DROP COLUMN IF EXISTS lead_time_days;
