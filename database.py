import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# Initialize connection. Uses st.cache_resource to only connect once.
@st.cache_resource
def init_connection():
    # Looks for a "mongo" dictionary inside your secrets management setup
    mongo_uri = st.secrets["mongo"]["uri"]
    return MongoClient(mongo_uri)

try:
    client = init_connection()
    # Name your database "home_expenses"
    db = client.home_expenses
    # Collection for storing individual expense records
    expenses_collection = db.expenses
except Exception as e:
    st.error(f"Error connecting to MongoDB: {e}")

def insert_expense(amount, category, description, date):
    """Inserts an expense record into MongoDB."""
    record = {
        "amount": float(amount),
        "category": category,
        "description": description,
        "date": datetime.combine(date, datetime.min.time()) # Keep it standard datetime format
    }
    return expenses_collection.insert_one(record)

def fetch_all_expenses():
    """Retrieves all expenses from the database."""
    # Convert cursor to list so it works seamlessly with Pandas DataFrames
    return list(expenses_collection.find())
