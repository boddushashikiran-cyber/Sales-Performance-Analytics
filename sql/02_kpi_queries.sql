-- Analytical queries used for reporting (run after 01_clean_join.sql).

-- 1) Overall KPIs
SELECT ROUND(SUM(revenue),2) AS revenue, ROUND(SUM(profit),2) AS profit,
       ROUND(100.0*SUM(profit)/SUM(revenue),2) AS profit_margin_pct,
       COUNT(DISTINCT order_id) AS orders, COUNT(DISTINCT customer_id) AS customers
FROM sales_clean;

-- 2) Monthly revenue & profit trend
SELECT month, ROUND(SUM(revenue),2) AS revenue, ROUND(SUM(profit),2) AS profit
FROM sales_clean GROUP BY month ORDER BY month;

-- 3) Regional performance
SELECT region, ROUND(SUM(revenue),2) AS revenue, ROUND(SUM(profit),2) AS profit,
       ROUND(100.0*SUM(profit)/SUM(revenue),2) AS margin_pct
FROM sales_clean GROUP BY region ORDER BY revenue DESC;

-- 4) Top 10 customers
SELECT customer_name, segment, ROUND(SUM(revenue),2) AS revenue
FROM sales_clean GROUP BY customer_id ORDER BY revenue DESC LIMIT 10;

-- 5) Month-over-month growth (window function)
SELECT month, revenue,
       ROUND(100.0*(revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month),2) AS mom_growth_pct
FROM (SELECT month, SUM(revenue) AS revenue FROM sales_clean GROUP BY month);
