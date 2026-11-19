# Power BI setup
1. Run `python pipeline.py`, then in Power BI Desktop: **Get Data > Text/CSV > `data/sales_clean.csv`**.
2. Add a date table: `Calendar = CALENDAR(MIN(sales_clean[order_date]), MAX(sales_clean[order_date]))` and relate it to `order_date`.
3. DAX measures:
```
Total Revenue   = SUM(sales_clean[revenue])
Total Profit    = SUM(sales_clean[profit])
Profit Margin % = DIVIDE([Total Profit], [Total Revenue])
Orders          = DISTINCTCOUNT(sales_clean[order_id])
Avg Order Value = DIVIDE([Total Revenue], [Orders])
Revenue LM      = CALCULATE([Total Revenue], DATEADD('Calendar'[Date], -1, MONTH))
MoM Growth %    = DIVIDE([Total Revenue] - [Revenue LM], [Revenue LM])
```
4. Visuals: KPI cards (Revenue, Profit, Margin, Orders), line chart (month vs Revenue/Profit), bar/map (region), donut (category), table (top customers), slicers (region, segment, month).
5. Save as `powerbi/Sales_Dashboard.pbix`, and add a screenshot to `docs/powerbi-preview.png`.
