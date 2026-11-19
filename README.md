# Sales Performance Analytics Dashboard 2025

A business intelligence project that analyses sales, profit, customer trends and regional performance.

**Live dashboard:** `https://<your-username>.github.io/<repo-name>/`

## What it does
- **Interactive dashboard** with KPIs, revenue trends, profit margins and regional sales performance (web version in `docs/`, Power BI version in `powerbi/`).
- **SQL** (`sql/`) cleans, joins and aggregates data from three business tables (orders, customers, products): removes duplicates and invalid rows, standardises text, and uses window functions for month-over-month growth.
- **Python (Pandas)** (`pipeline.py`) automates monthly reporting: it runs the SQL, aggregates results, and writes an Excel report plus the dashboard's data, replacing repetitive manual analysis.

## Tech stack
SQL (SQLite syntax) · Python (Pandas) · Power BI · Chart.js · GitHub Actions / Pages

## Project structure
```
data/        source CSVs (sample data) + cleaned sales_clean.csv
sql/         01_clean_join.sql, 02_kpi_queries.sql
pipeline.py  monthly reporting automation
generate_data.py  creates sample data
reports/     generated monthly Excel reports
docs/        web dashboard (deployed with GitHub Pages)
powerbi/     Power BI setup guide and DAX measures
.github/workflows/monthly-report.yml  auto-runs the report monthly
```

## Run locally
```bash
pip install -r requirements.txt
python generate_data.py            # optional: regenerate sample data
python pipeline.py                 # or: python pipeline.py --month 2025-06
python -m http.server -d docs 8000 # open http://localhost:8000
```

## Deploy
1. Push to GitHub. 2. **Settings > Pages > Deploy from branch > `main` / `/docs`**. 3. Your dashboard goes live in about a minute.

## Key results (sample data)
~3,960 clean orders, ₹30.5 L revenue, 26.9% profit margin, with a Q4 seasonal lift.
