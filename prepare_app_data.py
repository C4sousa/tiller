"""Create a compact weekly-demand file for the Streamlit app."""
from pathlib import Path
import pandas as pd

ROOT = Path.cwd()
SOURCE = ROOT / "data" / "order_data.csv"
OUTPUT_DIR = ROOT / "app" / "data"
OUTPUT = OUTPUT_DIR / "weekly_store_orders.csv"

if not SOURCE.exists():
    raise FileNotFoundError(f"Could not find: {SOURCE}")

print("Loading order data...")
orders = pd.read_csv(SOURCE, usecols=["id_store", "date_opened"])

orders["date_opened"] = pd.to_datetime(orders["date_opened"], errors="coerce")
orders = orders.dropna(subset=["id_store", "date_opened"]).copy()

orders["week"] = (
    orders["date_opened"]
    .dt.normalize()
    .sub(pd.to_timedelta(orders["date_opened"].dt.weekday, unit="D"))
)

print("Aggregating to weekly store-level demand...")
weekly = (
    orders.groupby(["id_store", "week"], as_index=False)
    .size()
    .rename(columns={"size": "orders"})
    .sort_values(["id_store", "week"])
)

weekly["id_store"] = weekly["id_store"].astype(str)
weekly["orders"] = weekly["orders"].astype(int)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
weekly.to_csv(OUTPUT, index=False)

print(f"\nCreated: {OUTPUT}")
print(f"Rows: {len(weekly):,}")
print(f"Stores: {weekly['id_store'].nunique():,}")
print(f"Date range: {weekly['week'].min().date()} to {weekly['week'].max().date()}")
print(f"File size: {OUTPUT.stat().st_size / 1024:.1f} KB")
