# PhonePe Transaction Insights — Setup Guide
### Labmentix Data Science Internship Project

---

## 📁 Project Files

| File | Purpose | Where to Run |
|------|---------|--------------|
| `phonepe_json_to_csv.py` | Clone repo + convert all JSONs to CSVs | Google Colab |
| `phonepe_dashboard.py` | Full Streamlit dashboard | Local / Cloud |
| `phonepe_report_generator.py` | Auto-generate PDF report with charts | Google Colab or Local |

---

## 🚀 Step-by-Step Instructions

### STEP 1 — Google Colab: Clone & Convert JSONs

Paste these cells in Colab **in order**:

```python
# Cell 1 — Clone the dataset
!git clone https://github.com/PhonePe/pulse.git
```

```python
# Cell 2 — Install dependencies
!pip install pandas
```

```python
# Cell 3 — Upload and run the converter
# (Upload phonepe_json_to_csv.py first via Files panel)
exec(open("phonepe_json_to_csv.py").read())
```

After running, you'll have a `phonepe_csvs/` folder with these files:
- `aggregated_transaction.csv`
- `aggregated_user.csv`
- `aggregated_insurance.csv`
- `map_transaction.csv`
- `map_user.csv`
- `map_insurance.csv`
- `top_transaction_district.csv`
- `top_transaction_pincode.csv`
- `top_user_district.csv`
- `top_user_pincode.csv`

**Download the entire `phonepe_csvs/` folder** (zip it in Colab):
```python
import shutil
shutil.make_archive("phonepe_csvs", "zip", "phonepe_csvs")
# Then download phonepe_csvs.zip from the Files panel
```

---

### STEP 2 — Generate PDF Report (Colab)

```python
# Cell — Install PDF libraries
!pip install reportlab matplotlib seaborn pandas

# Run the report generator
exec(open("phonepe_report_generator.py").read())
# Downloads phonepe_report.pdf
```

---

### STEP 3 — Run Streamlit Dashboard (Local)

```bash
# Install requirements
pip install streamlit pandas plotly

# Place phonepe_csvs/ folder in same directory as phonepe_dashboard.py
# Then run:
streamlit run phonepe_dashboard.py
```

The dashboard opens at: **http://localhost:8501**

---

### STEP 3 (Alternative) — Run on Colab using ngrok

```python
!pip install streamlit pyngrok plotly pandas
!ngrok authtoken YOUR_NGROK_TOKEN   # get free token at ngrok.com

from pyngrok import ngrok
import subprocess, threading

def run_streamlit():
    subprocess.run(["streamlit", "run", "phonepe_dashboard.py",
                    "--server.port", "8501", "--server.headless", "true"])

t = threading.Thread(target=run_streamlit, daemon=True)
t.start()

import time; time.sleep(3)
public_url = ngrok.connect(8501)
print("Dashboard URL:", public_url)
```

---

## 📊 Dashboard Pages

| Page | Charts Included |
|------|----------------|
| 🏠 Overview | KPI cards, YoY trend, type pie, top states bar |
| 💳 Transactions | Heatmap, grouped bar by type/year, box plots, trend lines |
| 👥 Users | Area chart, app opens, top states bar, treemap |
| 🛡️ Insurance | Pie chart, area growth, funnel top states |
| 🗺️ Geo Maps | India choropleth, district scatter bubble |
| 🏆 Top Performers | Districts, pincodes, user districts |
| 📈 Trend Analysis | QoQ growth bar, users vs app opens, correlation heatmap |

---

## 📦 Full Requirements

```
pandas
numpy
plotly
streamlit
matplotlib
seaborn
reportlab
```

Install all:
```bash
pip install pandas numpy plotly streamlit matplotlib seaborn reportlab
```

---

## 🗄️ Database Setup (Optional — MySQL/PostgreSQL)

To load CSVs into SQL:

```python
import pandas as pd
from sqlalchemy import create_engine

# MySQL example
engine = create_engine("mysql+pymysql://user:password@localhost/phonepe_db")

tables = [
    "aggregated_transaction", "aggregated_user", "aggregated_insurance",
    "map_transaction", "map_user", "map_insurance",
    "top_transaction_district", "top_transaction_pincode",
    "top_user_district", "top_user_pincode",
]
for table in tables:
    df = pd.read_csv(f"phonepe_csvs/{table}.csv")
    df.to_sql(table, engine, if_exists="replace", index=False)
    print(f"Loaded {table} → {len(df)} rows")
```

---

*PhonePe Transaction Insights | Labmentix Internship | Built with Python + Streamlit*
