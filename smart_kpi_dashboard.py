import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")

st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("📊 Smart KPI Dashboard")
st.markdown("Upload your Excel sales data to view KPIs and insights.")

info_col, sample_col = st.columns([3, 1])
with info_col:
    st.markdown("### 📥 Upload Your Sales Data")
    st.info(
        "ℹ️ **Required columns in your Excel file:**\n"
        "- `Date` (date of sale)\n"
        "- `Region` (sales region)\n"
        "- `Product` (product name)\n"
        "- `Sales` (numeric sales value)\n"
        "- `Quantity` (units sold)\n"
        "- `Discount (%)` (offered on sale)\n"
        "- `Profit` (sales minus base cost)\n"
        "- `Category` (Apparel, Accessories, etc.)\n"
        "- `Payment Method` (Cash, Credit Card, UPI, etc.)\n\n"
        "Make sure your file includes these columns for the dashboard to work correctly."
    )
with sample_col:
    import io
    sample_data = pd.DataFrame({
        "Date": ["2024-01-01", "2024-01-02"],
        "Region": ["North", "South"],
        "Product": ["A", "B"],
        "Sales": [1000, 1500],
        "Quantity": [10, 15],
        "Discount (%)": [5, 10],
        "Profit": [200, 300],
        "Category": ["Apparel", "Accessories"],
        "Payment Method": ["Cash", "Credit Card"]
    })
    sample_buffer = io.BytesIO()
    sample_data.to_excel(sample_buffer, index=False)
    sample_buffer.seek(0)
    st.download_button(
        label="Download Sample Excel File",
        data=sample_buffer,
        file_name="sample_sales_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])

    # --- Filters ---
    st.markdown("### 🔎 Filter Selection")
    filter_cols = st.columns(4)
    regions = df['Region'].unique() if 'Region' in df.columns else []
    selected_regions = filter_cols[0].multiselect("Select Region(s)", options=regions, default=regions)
    products = df['Product'].unique() if 'Product' in df.columns else []
    selected_products = filter_cols[1].multiselect("Select Product(s)", options=products, default=products)
    categories = df['Category'].unique() if 'Category' in df.columns else []
    selected_categories = filter_cols[2].multiselect("Select Category(s)", options=categories, default=categories)
    min_date = df['Date'].min() if 'Date' in df.columns else None
    max_date = df['Date'].max() if 'Date' in df.columns else None
    selected_dates = filter_cols[3].date_input(
        "Select Date Range",
        value=(min_date, max_date) if min_date is not None and max_date is not None else None,
        min_value=min_date,
        max_value=max_date
    ) if min_date is not None and max_date is not None else None

    filtered_df = df.copy()
    if selected_regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]
    if selected_products:
        filtered_df = filtered_df[filtered_df['Product'].isin(selected_products)]
    if selected_categories:
        filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]
    if selected_dates and isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1])
        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]

    # --- Calculated Columns ---
    if 'Sales' in filtered_df.columns and 'Discount (%)' in filtered_df.columns:
        filtered_df['Sales After Discount'] = filtered_df['Sales'] * (1 - filtered_df['Discount (%)'] / 100)
    else:
        filtered_df['Sales After Discount'] = np.nan

    # --- KPIs ---
    total_sales = filtered_df['Sales'].sum() if 'Sales' in filtered_df.columns else 0
    total_sales_after_discount = filtered_df['Sales After Discount'].sum() if 'Sales After Discount' in filtered_df.columns else 0
    avg_sales = filtered_df['Sales'].mean() if 'Sales' in filtered_df.columns and not filtered_df.empty else 0
    total_profit = filtered_df['Profit'].sum() if 'Profit' in filtered_df.columns else 0
    avg_profit = filtered_df['Profit'].mean() if 'Profit' in filtered_df.columns and not filtered_df.empty else 0
    num_transactions = len(filtered_df) if not filtered_df.empty else 0
    unique_products = filtered_df['Product'].nunique() if 'Product' in filtered_df.columns else 0
    top_product = (
        filtered_df.groupby('Product')['Sales'].sum().idxmax()
        if 'Product' in filtered_df.columns and not filtered_df.empty else "-"
    )
    top_region = (
        filtered_df.groupby('Region')['Sales'].sum().idxmax()
        if 'Region' in filtered_df.columns and not filtered_df.empty else "-"
    )

    st.markdown("### 📌 Key Performance Indicators")
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Total Sales", f"₹{total_sales:,.0f}")
    kpi2.metric("Sales After Discount", f"₹{total_sales_after_discount:,.0f}")
    kpi3.metric("Total Profit", f"₹{total_profit:,.0f}")
    kpi4.metric("Transactions", f"{num_transactions}")
    kpi5.metric("Unique Products", f"{unique_products}")

    # --- Summary/Insights Section ---
    st.markdown("### 📝 Summary & Insights")
    if not filtered_df.empty:
        st.success(
            f"""
            - **Top Region:** {top_region}
            - **Top Product:** {top_product}
            - **Highest Sales Day:** {filtered_df.loc[filtered_df['Sales'].idxmax(), 'Date'].strftime('%Y-%m-%d') if 'Sales' in filtered_df.columns else '-'}
            - **Average Sales per Transaction:** ₹{avg_sales:,.2f}
            - **Average Profit per Transaction:** ₹{avg_profit:,.2f}
            """
        )
    else:
        st.info("No data available for summary.")
        # --- Sales Analysis Section ---
    st.markdown("### 📈 Sales Analysis")
    classic1, classic2, classic3 = st.columns(3)

    with classic1:
        st.markdown("#### Sales by Region")
        if not filtered_df.empty and 'Region' in filtered_df.columns and 'Sales' in filtered_df.columns:
            sales_by_region = filtered_df.groupby('Region')['Sales'].sum()
            st.bar_chart(sales_by_region)
        else:
            st.info("No data for sales by region.")

    with classic2:
        st.markdown("#### Product Share")
        if not filtered_df.empty and 'Product' in filtered_df.columns and 'Sales' in filtered_df.columns:
            product_share = filtered_df.groupby('Product')['Sales'].sum()
            if product_share.sum() > 0:
                fig1, ax1 = plt.subplots(figsize=(4, 4))
                ax1.pie(product_share, labels=product_share.index, autopct='%1.1f%%', startangle=90)
                ax1.axis('equal')
                st.pyplot(fig1)
            else:
                st.info("No sales data for products.")
        else:
            st.info("No data for product share.")

    with classic3:
        st.markdown("#### Weekly Sales Trend")
        if not filtered_df.empty and 'Date' in filtered_df.columns and 'Sales' in filtered_df.columns:
            weekly_sales = filtered_df.resample('W', on='Date')['Sales'].sum()
            st.line_chart(weekly_sales)
        else:
            st.info("No data for weekly sales trend.")

    # --- Charts Section ---
    st.markdown("### 📊 Analysis Visualizations")
    chart1, chart2 = st.columns(2)

    # Profit Trends by Category or Region
    with chart1:
        st.markdown("#### Profit Trend by Category")
        if not filtered_df.empty and 'Date' in filtered_df.columns and 'Category' in filtered_df.columns:
            profit_cat = filtered_df.groupby(['Date', 'Category'])['Profit'].sum().reset_index()
            pivot = profit_cat.pivot(index='Date', columns='Category', values='Profit')
            st.line_chart(pivot)
        else:
            st.info("Not enough data for profit trend by category.")

    with chart2:
        st.markdown("#### Profit Trend by Region")
        if not filtered_df.empty and 'Date' in filtered_df.columns and 'Region' in filtered_df.columns:
            profit_reg = filtered_df.groupby(['Date', 'Region'])['Profit'].sum().reset_index()
            pivot = profit_reg.pivot(index='Date', columns='Region', values='Profit')
            st.line_chart(pivot)
        else:
            st.info("Not enough data for profit trend by region.")

    # Sales After Discounts Trend
    st.markdown("#### Sales After Discount Trend")
    if not filtered_df.empty and 'Date' in filtered_df.columns and 'Sales After Discount' in filtered_df.columns:
        sales_discount = filtered_df.groupby('Date')['Sales After Discount'].sum()
        st.line_chart(sales_discount)
    else:
        st.info("Not enough data for sales after discount trend.")

    # Most Common Payment Modes & Quantity vs. Revenue Correlation side by side
    chart3, chart4 = st.columns(2)

    with chart3:
        st.markdown("#### Most Common Payment Modes")
        if not filtered_df.empty and 'Payment Method' in filtered_df.columns:
            payment_counts = filtered_df['Payment Method'].value_counts()
            st.bar_chart(payment_counts)
        else:
            st.info("No data for payment methods.")

    with chart4:
        st.markdown("#### Quantity vs. Revenue Correlation")
        if not filtered_df.empty and 'Quantity' in filtered_df.columns and 'Sales' in filtered_df.columns:
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.scatter(filtered_df['Quantity'], filtered_df['Sales'], alpha=0.6)
            ax.set_xlabel('Quantity Sold')
            ax.set_ylabel('Sales Revenue')
            ax.set_title('Quantity vs. Revenue')
            st.pyplot(fig)
        else:
            st.info("Not enough data for quantity vs. revenue correlation.")

    # --- Data Table and Download ---
    st.markdown("### 🗃️ Data Table")
    with st.expander("View Raw Data"):
        st.dataframe(filtered_df)

    st.markdown("### 📥 Download Processed Data")
    st.download_button(
        label="Download CSV",
        data=filtered_df.to_csv(index=False),
        file_name="processed_data.csv",
        mime="text/csv"
    )
else:
    st.info("📥 Please upload an Excel file.")