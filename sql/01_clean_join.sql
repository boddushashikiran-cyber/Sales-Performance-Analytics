-- Cleans, joins and standardises the three source tables into one analytics table.
DROP TABLE IF EXISTS sales_clean;

CREATE TABLE sales_clean AS
SELECT
    order_id, order_date, month, customer_id, customer_name, segment, region,
    category, product_name, quantity, discount, revenue, cost,
    ROUND(revenue - cost, 2) AS profit
FROM (
    SELECT
        o.order_id,
        DATE(o.order_date)                          AS order_date,
        STRFTIME('%Y-%m', o.order_date)             AS month,
        c.customer_id,
        c.customer_name,
        c.segment,
        UPPER(SUBSTR(TRIM(c.region), 1, 1)) || LOWER(SUBSTR(TRIM(c.region), 2)) AS region,
        p.category,
        p.product_name,
        o.quantity,
        o.discount,
        ROUND(o.quantity * p.unit_price * (1 - o.discount), 2) AS revenue,
        ROUND(o.quantity * p.unit_cost, 2)                     AS cost
    FROM (SELECT DISTINCT * FROM orders)  o            -- remove duplicate rows
    JOIN customers c ON c.customer_id = o.customer_id  -- inner join drops rows with NULL customer
    JOIN products  p ON p.product_id  = o.product_id
    WHERE o.quantity > 0                               -- drop invalid quantities
);
