"""
E-Commerce Sales Analytics — Full Analysis
==========================================
Covers: Revenue trends, category performance, regional breakdown,
        payment methods, customer segmentation, returns analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")
os.makedirs("outputs", exist_ok=True)

# ── Palette & style ──────────────────────────────────────────────────────────
PALETTE = ["#4361EE", "#3A0CA3", "#7209B7", "#F72585", "#4CC9F0", "#06D6A0"]
sns.set_theme(style="whitegrid", palette=PALETTE)
plt.rcParams.update({"font.family": "DejaVu Sans", "figure.dpi": 130})

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("data/ecommerce_sales.csv", parse_dates=["order_date"])
print(f"Dataset: {df.shape[0]:,} orders | {df['revenue'].sum():,.0f} ₹ total revenue\n")

# ════════════════════════════════════════════════════════════════════════════
# 1. MONTHLY REVENUE TREND
# ════════════════════════════════════════════════════════════════════════════
monthly = (df.groupby("month")["revenue"]
             .sum()
             .reset_index()
             .rename(columns={"revenue": "total_revenue"}))
month_labels = ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"]
monthly["month_name"] = monthly["month"].apply(lambda x: month_labels[x-1])

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(monthly["month"], monthly["total_revenue"], alpha=0.15, color=PALETTE[0])
ax.plot(monthly["month"], monthly["total_revenue"], marker="o", color=PALETTE[0],
        linewidth=2.5, markersize=7)
ax.set_xticks(monthly["month"])
ax.set_xticklabels(monthly["month_name"])
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M"))
ax.set_title("Monthly Revenue Trend — 2023", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Month"); ax.set_ylabel("Revenue")
plt.tight_layout()
plt.savefig("outputs/01_monthly_revenue.png"); plt.close()
print("✅ Chart 1 saved — Monthly Revenue Trend")

# ════════════════════════════════════════════════════════════════════════════
# 2. REVENUE BY CATEGORY
# ════════════════════════════════════════════════════════════════════════════
cat_rev = (df.groupby("category")["revenue"]
             .sum()
             .sort_values(ascending=True))

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(cat_rev.index, cat_rev.values, color=PALETTE[:len(cat_rev)], height=0.6)
for bar, val in zip(bars, cat_rev.values):
    ax.text(val + 50000, bar.get_y() + bar.get_height()/2,
            f"₹{val/1e6:.1f}M", va="center", fontsize=9)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.0f}M"))
ax.set_title("Total Revenue by Category", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Revenue")
plt.tight_layout()
plt.savefig("outputs/02_category_revenue.png"); plt.close()
print("✅ Chart 2 saved — Category Revenue")

# ════════════════════════════════════════════════════════════════════════════
# 3. REGION-WISE REVENUE (PIE)
# ════════════════════════════════════════════════════════════════════════════
reg_rev = df.groupby("region")["revenue"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(
    reg_rev.values, labels=reg_rev.index, autopct="%1.1f%%",
    colors=PALETTE, startangle=140,
    wedgeprops={"edgecolor": "white", "linewidth": 2})
for at in autotexts:
    at.set_fontsize(9); at.set_color("white"); at.set_fontweight("bold")
ax.set_title("Revenue Distribution by Region", fontsize=15, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig("outputs/03_region_revenue.png"); plt.close()
print("✅ Chart 3 saved — Region Revenue")

# ════════════════════════════════════════════════════════════════════════════
# 4. PAYMENT METHOD PREFERENCE
# ════════════════════════════════════════════════════════════════════════════
pay_counts = df["payment_method"].value_counts()

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(pay_counts.index, pay_counts.values, color=PALETTE, width=0.55)
for bar, val in zip(bars, pay_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 15,
            f"{val:,}", ha="center", fontsize=9, fontweight="bold")
ax.set_title("Payment Method Preference", fontsize=15, fontweight="bold", pad=12)
ax.set_ylabel("Number of Orders")
ax.set_xlabel("Payment Method")
plt.tight_layout()
plt.savefig("outputs/04_payment_methods.png"); plt.close()
print("✅ Chart 4 saved — Payment Methods")

# ════════════════════════════════════════════════════════════════════════════
# 5. HEATMAP — Category × Region Revenue
# ════════════════════════════════════════════════════════════════════════════
pivot = df.pivot_table(values="revenue", index="category",
                       columns="region", aggfunc="sum")

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(pivot / 1e6, annot=True, fmt=".1f", cmap="YlOrRd",
            linewidths=0.5, ax=ax, cbar_kws={"label": "Revenue (₹M)"})
ax.set_title("Revenue Heatmap — Category × Region (₹ Millions)",
             fontsize=14, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig("outputs/05_heatmap_cat_region.png"); plt.close()
print("✅ Chart 5 saved — Heatmap")

# ════════════════════════════════════════════════════════════════════════════
# 6. RATING DISTRIBUTION
# ════════════════════════════════════════════════════════════════════════════
rating_counts = df["rating"].value_counts().sort_index()
colors_r = ["#EF233C", "#F77F00", "#FCBF49", "#06D6A0", "#4361EE"]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar([str(r) + "★" for r in rating_counts.index],
              rating_counts.values, color=colors_r, width=0.55)
for bar, val in zip(bars, rating_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 10,
            f"{val}", ha="center", fontsize=9, fontweight="bold")
ax.set_title("Customer Rating Distribution", fontsize=15, fontweight="bold", pad=12)
ax.set_ylabel("Number of Orders"); ax.set_xlabel("Rating")
plt.tight_layout()
plt.savefig("outputs/06_rating_distribution.png"); plt.close()
print("✅ Chart 6 saved — Ratings")

# ════════════════════════════════════════════════════════════════════════════
# 7. WEEKLY SALES PATTERN
# ════════════════════════════════════════════════════════════════════════════
day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
weekly = df.groupby("day_of_week")["revenue"].mean().reindex(day_order)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(weekly.index, weekly.values,
       color=[PALETTE[i % len(PALETTE)] for i in range(7)], width=0.6)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
ax.set_title("Average Daily Revenue by Day of Week", fontsize=15, fontweight="bold", pad=12)
ax.set_ylabel("Avg Revenue per Order"); ax.set_xlabel("Day")
plt.tight_layout()
plt.savefig("outputs/07_weekly_pattern.png"); plt.close()
print("✅ Chart 7 saved — Weekly Pattern")

# ════════════════════════════════════════════════════════════════════════════
# 8. SUMMARY KPI TABLE
# ════════════════════════════════════════════════════════════════════════════
kpis = {
    "Total Orders": f"{len(df):,}",
    "Total Revenue": f"₹{df['revenue'].sum():,.0f}",
    "Avg Order Value": f"₹{df['revenue'].mean():,.0f}",
    "Return Rate": f"{df['is_returned'].mean()*100:.1f}%",
    "Avg Rating": f"{df['rating'].mean():.2f} / 5",
    "Top Category": df.groupby('category')['revenue'].sum().idxmax(),
    "Top Region": df.groupby('region')['revenue'].sum().idxmax(),
    "Top Payment": df['payment_method'].mode()[0],
}
kpi_df = pd.DataFrame(list(kpis.items()), columns=["KPI", "Value"])
kpi_df.to_csv("outputs/kpi_summary.csv", index=False)
print("\n📊 KPI Summary:")
print(kpi_df.to_string(index=False))
print("\n🎉 All outputs saved to /outputs/")
