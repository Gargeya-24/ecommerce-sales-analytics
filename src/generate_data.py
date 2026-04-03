import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# --- Config ---
N = 5000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2023, 12, 31)

CATEGORIES = {
    "Electronics": {"avg_price": 8500, "std": 3000},
    "Clothing": {"avg_price": 1200, "std": 500},
    "Books": {"avg_price": 400, "std": 150},
    "Home & Kitchen": {"avg_price": 2200, "std": 800},
    "Sports": {"avg_price": 1800, "std": 700},
    "Beauty": {"avg_price": 900, "std": 300},
}

REGIONS = ["North", "South", "East", "West", "Central"]
PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Net Banking", "COD"]
PAYMENT_WEIGHTS = [0.40, 0.22, 0.18, 0.10, 0.10]

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days),
                             hours=random.randint(0, 23),
                             minutes=random.randint(0, 59))

rows = []
for i in range(N):
    category = random.choice(list(CATEGORIES.keys()))
    cfg = CATEGORIES[category]
    price = max(100, np.random.normal(cfg["avg_price"], cfg["std"]))
    qty = np.random.choice([1, 2, 3, 4, 5], p=[0.55, 0.25, 0.10, 0.06, 0.04])
    discount = np.random.choice([0, 5, 10, 15, 20], p=[0.40, 0.25, 0.20, 0.10, 0.05])
    revenue = round(price * qty * (1 - discount / 100), 2)
    order_date = random_date(START_DATE, END_DATE)
    
    rows.append({
        "order_id": f"ORD{100000 + i}",
        "order_date": order_date,
        "category": category,
        "product_price": round(price, 2),
        "quantity": qty,
        "discount_pct": discount,
        "revenue": revenue,
        "region": random.choice(REGIONS),
        "payment_method": random.choices(PAYMENT_METHODS, weights=PAYMENT_WEIGHTS)[0],
        "customer_age": np.random.randint(18, 65),
        "is_returned": np.random.choice([0, 1], p=[0.92, 0.08]),
        "rating": np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.08, 0.17, 0.40, 0.30]),
    })

df = pd.DataFrame(rows)
df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.strftime("%b")
df["day_of_week"] = df["order_date"].dt.day_name()
df["quarter"] = df["order_date"].dt.quarter

os.makedirs("data", exist_ok=True)
df.to_csv("data/ecommerce_sales.csv", index=False)
print(f"✅ Dataset generated: {len(df)} rows → data/ecommerce_sales.csv")
print(df.head())
