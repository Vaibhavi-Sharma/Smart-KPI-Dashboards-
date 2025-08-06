# Smart-KPI-Dashboards-
# 📊 Smart KPI Dashboard

An interactive, Excel-powered dashboard built with **Streamlit** and **Pandas** for visualizing and analyzing sales data.

This tool allows business users and analysts to:
- Upload structured sales data
- Apply dynamic filters (date range, region, product, category)
- View key performance indicators (KPIs)
- Explore visual insights like sales trends, product shares, and profit distribution
- Export processed data for reports or presentations

---

## 🚀 Features

✅ Upload Excel file and auto-read structured sales data  
✅ Filters for Region, Product, Category, Date Range  
✅ Key Metrics:  
- Total Sales  
- Sales After Discount  
- Total Profit  
- Unique Products  
- # of Transactions  

✅ Auto-generated insights:
- Top performing region and product  
- Highest sales day  
- Average per transaction revenue and profit  

✅ Visualizations:
- Bar: Sales by Region  
- Pie: Product Share  
- Line: Weekly Sales Trend  
- Line: Profit Trends by Category/Region  
- Line: Sales After Discount  
- Bar: Most Common Payment Methods  
- Scatter: Quantity vs Revenue Correlation  

✅ Export filtered data as downloadable CSV  
✅ Download sample data template for quick testing

---

## 📁 Sample Excel Structure

Your uploaded Excel file should have the following columns:

| Column Name       | Description                                 |
|-------------------|---------------------------------------------|
| `Date`            | Date of the sale                            |
| `Region`          | Sales region (e.g., North, South)           |
| `Product`         | Product name                                |
| `Sales`           | Sale value (before discount)                |
| `Quantity`        | Units sold                                  |
| `Discount (%)`    | Discount applied (e.g., 10%)                |
| `Profit`          | Net profit from the sale                    |
| `Category`        | Product category (e.g., Apparel)            |
| `Payment Method`  | Mode of payment (Cash, UPI, Credit Card)    |

You can download a ready-to-use sample from within the app UI.

---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io/) – interactive UI
- [Pandas](https://pandas.pydata.org/) – data cleaning and analysis
- [Matplotlib](https://matplotlib.org/) – for custom plots
- [OpenPyXL](https://openpyxl.readthedocs.io/) – Excel reading support (if needed)

---

## ▶️ How to Run Locally

### 1. Clone this repo
bash
git clone https://github.com/your-username/kpi-dashboard.git
cd kpi-dashboard
### 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
### 3. Install dependencies
pip install -r requirements.txt
### 4. Run the app
streamlit run smart_kpi_dashboard.py
