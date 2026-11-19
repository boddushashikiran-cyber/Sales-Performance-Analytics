"""Monthly sales reporting automation: SQL (clean + join) -> Pandas (aggregate) -> Excel report + dashboard data.

Usage:  python pipeline.py              # report for the latest month in the data
        python pipeline.py --month 2025-06
"""
import argparse, json, sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).parent

def load_clean() -> pd.DataFrame:
    con = sqlite3.connect(":memory:")
    for t in ("customers", "products", "orders"):
        pd.read_csv(ROOT / "data" / f"{t}.csv").to_sql(t, con, index=False)
    con.executescript((ROOT / "sql" / "01_clean_join.sql").read_text())
    return pd.read_sql("SELECT * FROM sales_clean", con)

def summarise(df: pd.DataFrame) -> dict:
    grp = lambda col: (df.groupby(col)[["revenue", "profit"]].sum().round(2)
                         .assign(margin_pct=lambda x: (x.profit / x.revenue * 100).round(2))
                         .sort_values("revenue", ascending=False).reset_index())
    monthly = df.groupby("month")[["revenue", "profit"]].sum().round(2)
    monthly["mom_growth_pct"] = (monthly.revenue.pct_change() * 100).round(2)
    return {"monthly": monthly.reset_index(), "region": grp("region"), "category": grp("category"),
            "segment": grp("segment"),
            "top_customers": df.groupby(["customer_name", "segment"]).revenue.sum().round(2)
                               .nlargest(10).reset_index()}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--month")
    month = ap.parse_args().month
    df = load_clean()
    month = month or df.month.max()
    s = summarise(df)

    # 1) Monthly Excel report
    sub = df[df.month == month]
    out = ROOT / "reports" / f"sales_report_{month}.xlsx"
    with pd.ExcelWriter(out) as xl:
        pd.DataFrame({"Metric": ["Revenue", "Profit", "Profit margin %", "Orders", "Customers"],
                      "Value": [round(sub.revenue.sum(), 2), round(sub.profit.sum(), 2),
                                round(sub.profit.sum() / sub.revenue.sum() * 100, 2),
                                sub.order_id.nunique(), sub.customer_id.nunique()]}).to_excel(xl, sheet_name="Summary", index=False)
        for name in ("region", "category", "segment"):
            sub.groupby(name)[["revenue", "profit"]].sum().round(2).sort_values("revenue", ascending=False).to_excel(xl, sheet_name=name.title())
        s["monthly"].to_excel(xl, sheet_name="Monthly Trend", index=False)
    df.to_csv(ROOT / "data" / "sales_clean.csv", index=False)  # import this file into Power BI

    # 2) Data for the web dashboard
    tot = {"revenue": df.revenue.sum(), "profit": df.profit.sum(), "orders": df.order_id.nunique(),
           "customers": df.customer_id.nunique()}
    tot["margin_pct"] = tot["profit"] / tot["revenue"] * 100
    tot["avg_order_value"] = tot["revenue"] / tot["orders"]
    payload = {"kpis": {k: round(float(v), 2) for k, v in tot.items()},
               **{k: v.to_dict("records") for k, v in s.items()}}
    (ROOT / "docs" / "data.js").write_text("window.DASH = " + json.dumps(payload, allow_nan=False) if False else json.dumps(payload).replace("NaN", "null") + ";")
    print(f"Done. Report: {out.relative_to(ROOT)} | dashboard data: docs/data.js | rows analysed: {len(df)}")

if __name__ == "__main__":
    main()
