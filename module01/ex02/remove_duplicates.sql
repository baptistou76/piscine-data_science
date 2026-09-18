-- Remove duplicate rows from customers
-- Two rows are duplicates when all columns except event_time
-- are identical and their timestamps differ by at most 1 second.

CREATE TEMP TABLE customers_clean AS
WITH ordered_events AS (
    SELECT
        event_time,
        event_type,
        product_id,
        price,
        user_id,
        user_session,
        LAG(event_time) OVER (
            PARTITION BY
                event_type,
                product_id,
                price,
                user_id,
                user_session
            ORDER BY event_time
        ) AS previous_event_time
    FROM customers
)
SELECT
    event_time,
    event_type,
    product_id,
    price,
    user_id,
    user_session
FROM ordered_events
WHERE previous_event_time IS NULL
   OR event_time - previous_event_time > INTERVAL '1 second';


-- Replace customers with the cleaned data.

DELETE FROM customers;

INSERT INTO customers (
    event_time,
    event_type,
    product_id,
    price,
    user_id,
    user_session
)
SELECT
    event_time,
    event_type,
    product_id,
    price,
    user_id,
    user_session
FROM customers_clean;