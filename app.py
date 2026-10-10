import streamlit as st
import pandas as pd
import plotly.express as px
from database import insert_expense, fetch_all_expenses
from datetime import datetime

# App Configuration
st.set_page_config(page_title="Home Expense Tracker", layout="wide")
st.title("🏡 Home Expense Tracker & Reporting Dashboard")

# Define categories
CATEGORIES = ["Groceries", "Utilities", "Rent/Mortgage", "Entertainment", "Health & Medical", "Transport", "Others"]

# Create a clean layout with 2 columns: Entry Form and Data Insights
col1, col2 = st.columns([1, 2])

# --- COLUMN 1: EXPENSE DATA ENTRY ---
with col1:
    st.header("➕ Add New Expense")
    with st.form("expense_form", clear_on_submit=True):
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
        category = st.selectbox("Category", CATEGORIES)
        description = st.text_input("Description / Notes")
        date = st.date_input("Date of Expense", datetime.today())
        
        submit_button = st.form_submit_button("Save Expense")
        
        if submit_button:
            if amount > 0:
                insert_expense(amount, category, description, date)
                st.success(f"Successfully recorded ${amount:.2f} for {category}!")
                # Force rerun to immediately display updated insights
                st.rerun()
            else:
                st.error("Please enter a valid amount.")

# --- COLUMN 2: MONTHLY REPORTING & ANALYTICS ---
with col2:
    st.header("📊 Financial Reports & Insights")
    
    raw_data = fetch_all_expenses()
    
    if not raw_data:
        st.info("No expense data recorded yet. Fill out the form on the left to get started!")
    else:
        # Convert NoSQL documents list directly to a DataFrame
        df = pd.DataFrame(raw_data)
        
        # Format columns for display
        df['date'] = pd.to_datetime(df['date'])
        df['Month-Year'] = df['date'].dt.strftime('%B %Y')
        
        # Month Filter Widget
        unique_months = df['Month-Year'].unique()
        selected_month = st.selectbox("Select Month for Report", unique_months)
        
        # Filter down data to selected month
        filtered_df = df[df['Month-Year'] == selected_month]
        
        # 1. Total Metrics summary
        total_monthly_spent = filtered_df['amount'].sum()
        st.metric(label=f"Total Spending for {selected_month}", value=f"${total_monthly_spent:,.2f}")
        
        # 2. Interactive Charts
        tab1, tab2 = st.tabs(["Category Summary Chart", "Detailed Log Matrix"])
        
        with tab1:
            # Group expenditures to plot breakdowns
            cat_summary = filtered_df.groupby("category")["amount"].sum().reset_index()
            
            fig = px.pie(
                cat_summary, 
                values='amount', 
                names='category', 
                title=f"Spending Breakdown: {selected_month}",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            # Clean viewable dataset omitting internal MongoDB _id fields
            display_df = filtered_df[['date', 'category', 'amount', 'description']].sort_values(by="date", ascending=False)
            display_df['date'] = display_df['date'].dt.date
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
