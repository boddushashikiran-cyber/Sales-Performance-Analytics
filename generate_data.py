"""Creates realistic sample business tables (with some deliberately dirty rows) in /data."""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)

regions = ["North", "South", "East", "West", "Central"]
segments = ["Consumer", "Corporate", "Small Business"]
cats = {"Technology": [("Laptop", 900, 650), ("Smartphone", 600, 420), ("Monitor", 250, 170), ("Headset", 80, 45)],
        "Furniture": [("Office Chair", 220, 140), ("Standing Desk", 480, 330), ("Bookcase", 150, 95)],
        "Office Supplies": [("Notebook Pack", 20, 9), ("Printer Paper", 35, 22), ("Pen Set", 15, 6), ("Binder", 12, 5)]}

products = pd.DataFrame(
    [(i + 1, c, n, p, k) for i, (c, n, p, k) in enumerate((c, *x) for c, v in cats.items() for x in v)],
    columns=["product_id", "category", "product_name", "unit_price", "unit_cost"])

customers = pd.DataFrame({
    "customer_id": range(1, 301),
    "customer_name": [f"Customer {i:03d}" for i in range(1, 301)],
    "segment": rng.choice(segments, 300, p=[.5, .3, .2]),
    "region": rng.choice(regions, 300, p=[.2, .2, .25, .25, .1]),
    "city": rng.choice(["Hyderabad", "Mumbai", "Delhi", "Chennai", "Pune", "Kolkata", "Bengaluru"], 300)})

n = 4000
dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D")
month_boost = rng.random(n) < (0.5 * (dates.month.isin([10, 11, 12])))  # seasonal Q4 lift
orders = pd.DataFrame({
    "order_id": range(10001, 10001 + n),
    "order_date": dates.strftime("%Y-%m-%d"),
    "customer_id": rng.integers(1, 301, n),
    "product_id": rng.integers(1, len(products) + 1, n),
    "quantity": rng.integers(1, 6, n) + month_boost.astype(int),
    "discount": rng.choice([0, 0, 0, .05, .1, .2], n)})

# dirty data for the SQL cleaning step
orders = pd.concat([orders, orders.sample(40, random_state=1)])           # duplicates
orders.loc[orders.sample(25, random_state=2).index, "customer_id"] = None  # missing keys
orders.loc[orders.sample(15, random_state=3).index, "quantity"] = 0        # invalid qty
customers["region"] = customers["region"].map(lambda r: rng.choice([r, r.upper(), f" {r.lower()} "], p=[.8, .1, .1]))

customers.to_csv("data/customers.csv", index=False)
products.to_csv("data/products.csv", index=False)
orders.to_csv("data/orders.csv", index=False)
print("Created data/customers.csv, products.csv, orders.csv")
