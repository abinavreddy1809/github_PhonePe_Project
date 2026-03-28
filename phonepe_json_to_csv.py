"""
==============================================================
PhonePe Pulse - JSON to CSV Converter
Run this in Google Colab FIRST before anything else.
==============================================================
"""

# ── STEP 0: Install & Clone ────────────────────────────────
# Run this cell in Colab:
# !git clone https://github.com/PhonePe/pulse.git
# !pip install pandas

import os
import json
import pandas as pd

BASE_PATH = "pulse/data"  # adjust if your clone path differs
OUTPUT_DIR = "phonepe_csvs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ══════════════════════════════════════════════════════════════
#  HELPER
# ══════════════════════════════════════════════════════════════
def save_csv(df: pd.DataFrame, name: str):
    path = os.path.join(OUTPUT_DIR, f"{name}.csv")
    df.to_csv(path, index=False)
    print(f"  ✅  Saved {name}.csv  ({len(df):,} rows)")
    return path


# ══════════════════════════════════════════════════════════════
#  1. AGGREGATED / TRANSACTION
# ══════════════════════════════════════════════════════════════
def parse_aggregated_transaction():
    rows = []
    root = os.path.join(BASE_PATH, "aggregated", "transaction", "country", "india", "state")
    for state in os.listdir(root):
        state_path = os.path.join(root, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for quarter_file in os.listdir(year_path):
                quarter = quarter_file.replace(".json", "")
                with open(os.path.join(year_path, quarter_file)) as f:
                    data = json.load(f)
                for txn in data.get("data", {}).get("transactionData", []):
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": int(quarter),
                        "Transaction_Type": txn["name"],
                        "Transaction_Count": txn["paymentInstruments"][0]["count"],
                        "Transaction_Amount": txn["paymentInstruments"][0]["amount"],
                    })
    return save_csv(pd.DataFrame(rows), "aggregated_transaction")


# ══════════════════════════════════════════════════════════════
#  2. AGGREGATED / USER
# ══════════════════════════════════════════════════════════════
def parse_aggregated_user():
    rows = []
    root = os.path.join(BASE_PATH, "aggregated", "user", "country", "india", "state")
    for state in os.listdir(root):
        state_path = os.path.join(root, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for quarter_file in os.listdir(year_path):
                quarter = quarter_file.replace(".json", "")
                with open(os.path.join(year_path, quarter_file)) as f:
                    data = json.load(f)
                d = data.get("data", {})
                reg = d.get("aggregated", {})
                rows.append({
                    "State": state, "Year": int(year), "Quarter": int(quarter),
                    "Registered_Users": reg.get("registeredUsers", 0),
                    "App_Opens": reg.get("appOpens", 0),
                })
                for brand_info in d.get("usersByDevice", []) or []:
                    rows_brand = {
                        "State": state, "Year": int(year), "Quarter": int(quarter),
                        "Brand": brand_info.get("brand"),
                        "User_Count": brand_info.get("count"),
                        "Percentage": brand_info.get("percentage"),
                    }
    df = pd.DataFrame(rows)
    return save_csv(df, "aggregated_user")


# ══════════════════════════════════════════════════════════════
#  3. AGGREGATED / INSURANCE
# ══════════════════════════════════════════════════════════════
def parse_aggregated_insurance():
    rows = []
    root = os.path.join(BASE_PATH, "aggregated", "insurance", "country", "india", "state")
    if not os.path.exists(root):
        print("  ⚠️  Insurance aggregated folder not found – skipping.")
        return
    for state in os.listdir(root):
        state_path = os.path.join(root, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for quarter_file in os.listdir(year_path):
                quarter = quarter_file.replace(".json", "")
                with open(os.path.join(year_path, quarter_file)) as f:
                    data = json.load(f)
                for txn in data.get("data", {}).get("transactionData", []):
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": int(quarter),
                        "Insurance_Type": txn["name"],
                        "Transaction_Count": txn["paymentInstruments"][0]["count"],
                        "Transaction_Amount": txn["paymentInstruments"][0]["amount"],
                    })
    save_csv(pd.DataFrame(rows), "aggregated_insurance")


# ══════════════════════════════════════════════════════════════
#  4. MAP / TRANSACTION
# ══════════════════════════════════════════════════════════════
def parse_map_transaction():
    rows = []
    root = os.path.join(BASE_PATH, "map", "transaction", "hover", "country", "india", "state")
    for state in os.listdir(root):
        state_path = os.path.join(root, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for quarter_file in os.listdir(year_path):
                quarter = quarter_file.replace(".json", "")
                with open(os.path.join(year_path, quarter_file)) as f:
                    data = json.load(f)
                for dist in data.get("data", {}).get("hoverDataList", []):
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": int(quarter),
                        "District": dist["name"],
                        "Transaction_Count": dist["metric"][0]["count"],
                        "Transaction_Amount": dist["metric"][0]["amount"],
                    })
    save_csv(pd.DataFrame(rows), "map_transaction")


# ══════════════════════════════════════════════════════════════
#  5. MAP / USER
# ══════════════════════════════════════════════════════════════
def parse_map_user():
    rows = []
    root = os.path.join(BASE_PATH, "map", "user", "hover", "country", "india", "state")
    for state in os.listdir(root):
        state_path = os.path.join(root, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for quarter_file in os.listdir(year_path):
                quarter = quarter_file.replace(".json", "")
                with open(os.path.join(year_path, quarter_file)) as f:
                    data = json.load(f)
                for dist in data.get("data", {}).get("hoverData", {}).items():
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": int(quarter),
                        "District": dist[0],
                        "Registered_Users": dist[1].get("registeredUsers", 0),
                        "App_Opens": dist[1].get("appOpens", 0),
                    })
    save_csv(pd.DataFrame(rows), "map_user")


# ══════════════════════════════════════════════════════════════
#  6. MAP / INSURANCE
# ══════════════════════════════════════════════════════════════
def parse_map_insurance():
    rows = []
    root = os.path.join(BASE_PATH, "map", "insurance", "hover", "country", "india", "state")
    if not os.path.exists(root):
        print("  ⚠️  Insurance map folder not found – skipping.")
        return
    for state in os.listdir(root):
        state_path = os.path.join(root, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for quarter_file in os.listdir(year_path):
                quarter = quarter_file.replace(".json", "")
                with open(os.path.join(year_path, quarter_file)) as f:
                    data = json.load(f)
                for dist in data.get("data", {}).get("hoverDataList", []):
                    rows.append({
                        "State": state, "Year": int(year), "Quarter": int(quarter),
                        "District": dist["name"],
                        "Transaction_Count": dist["metric"][0]["count"],
                        "Transaction_Amount": dist["metric"][0]["amount"],
                    })
    save_csv(pd.DataFrame(rows), "map_insurance")


# ══════════════════════════════════════════════════════════════
#  7. TOP / TRANSACTION
# ══════════════════════════════════════════════════════════════
def parse_top_transaction():
    rows_state, rows_dist, rows_pin = [], [], []
    root = os.path.join(BASE_PATH, "top", "transaction", "country", "india", "state")
    for state in os.listdir(root):
        state_path = os.path.join(root, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for quarter_file in os.listdir(year_path):
                quarter = quarter_file.replace(".json", "")
                with open(os.path.join(year_path, quarter_file)) as f:
                    data = json.load(f)
                d = data.get("data", {})
                for dist in d.get("districts", []) or []:
                    rows_dist.append({
                        "State": state, "Year": int(year), "Quarter": int(quarter),
                        "District": dist["entityName"],
                        "Transaction_Count": dist["metric"]["count"],
                        "Transaction_Amount": dist["metric"]["amount"],
                    })
                for pin in d.get("pincodes", []) or []:
                    rows_pin.append({
                        "State": state, "Year": int(year), "Quarter": int(quarter),
                        "Pincode": pin["entityName"],
                        "Transaction_Count": pin["metric"]["count"],
                        "Transaction_Amount": pin["metric"]["amount"],
                    })
    save_csv(pd.DataFrame(rows_dist), "top_transaction_district")
    save_csv(pd.DataFrame(rows_pin), "top_transaction_pincode")


# ══════════════════════════════════════════════════════════════
#  8. TOP / USER
# ══════════════════════════════════════════════════════════════
def parse_top_user():
    rows_dist, rows_pin = [], []
    root = os.path.join(BASE_PATH, "top", "user", "country", "india", "state")
    for state in os.listdir(root):
        state_path = os.path.join(root, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for quarter_file in os.listdir(year_path):
                quarter = quarter_file.replace(".json", "")
                with open(os.path.join(year_path, quarter_file)) as f:
                    data = json.load(f)
                d = data.get("data", {})
                for dist in d.get("districts", []) or []:
                    rows_dist.append({
                        "State": state, "Year": int(year), "Quarter": int(quarter),
                        "District": dist["name"],
                        "Registered_Users": dist["registeredUsers"],
                    })
                for pin in d.get("pincodes", []) or []:
                    rows_pin.append({
                        "State": state, "Year": int(year), "Quarter": int(quarter),
                        "Pincode": pin["name"],
                        "Registered_Users": pin["registeredUsers"],
                    })
    save_csv(pd.DataFrame(rows_dist), "top_user_district")
    save_csv(pd.DataFrame(rows_pin), "top_user_pincode")


# ══════════════════════════════════════════════════════════════
#  9. TOP / INSURANCE
# ══════════════════════════════════════════════════════════════
def parse_top_insurance():
    rows_dist, rows_pin = [], []
    root = os.path.join(BASE_PATH, "top", "insurance", "country", "india", "state")
    if not os.path.exists(root):
        print("  ⚠️  Insurance top folder not found – skipping.")
        return
    for state in os.listdir(root):
        state_path = os.path.join(root, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for quarter_file in os.listdir(year_path):
                quarter = quarter_file.replace(".json", "")
                with open(os.path.join(year_path, quarter_file)) as f:
                    data = json.load(f)
                d = data.get("data", {})
                for dist in d.get("districts", []) or []:
                    rows_dist.append({
                        "State": state, "Year": int(year), "Quarter": int(quarter),
                        "District": dist["entityName"],
                        "Transaction_Count": dist["metric"]["count"],
                        "Transaction_Amount": dist["metric"]["amount"],
                    })
                for pin in d.get("pincodes", []) or []:
                    rows_pin.append({
                        "State": state, "Year": int(year), "Quarter": int(quarter),
                        "Pincode": pin["entityName"],
                        "Transaction_Count": pin["metric"]["count"],
                        "Transaction_Amount": pin["metric"]["amount"],
                    })
    save_csv(pd.DataFrame(rows_dist), "top_insurance_district")
    save_csv(pd.DataFrame(rows_pin), "top_insurance_pincode")


# ══════════════════════════════════════════════════════════════
#  RUN ALL
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("\n🚀  PhonePe Pulse — JSON → CSV Converter\n" + "=" * 50)
    print("\n📦  Aggregated Tables")
    parse_aggregated_transaction()
    parse_aggregated_user()
    parse_aggregated_insurance()

    print("\n🗺️  Map Tables")
    parse_map_transaction()
    parse_map_user()
    parse_map_insurance()

    print("\n🏆  Top Tables")
    parse_top_transaction()
    parse_top_user()
    parse_top_insurance()

    print(f"\n✅  All CSVs saved to → ./{OUTPUT_DIR}/")
    print("   Files generated:")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        size = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / 1024
        print(f"   • {f:45s}  {size:8.1f} KB")
