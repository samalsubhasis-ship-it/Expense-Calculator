import os
from datetime import date, datetime
from pymongo import MongoClient

# 1. Initialize variables globally
client = None
db = None
expenses_collection = None


def init_db():
    global client, db, expenses_collection

    # 2. Get the connection URI (e.g., from environment variables)
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

    try:
        client = MongoClient(mongo_uri)
        db = client["expense_tracker"]  # Your database name
        expenses_collection = db["expenses"]  # Your collection name
        print("Connected to MongoDB successfully.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")


# 3. Ensure this runs when the module is imported
init_db()


def insert_expense(amount, category, description, expense_date):
    if expenses_collection is None:
        raise RuntimeError("Database collection 'expenses_collection' is not initialized. Check your connection setup.")

    if expense_date is None:
        expense_date = date.today()

    if isinstance(expense_date, datetime):
        expense_date = expense_date.date()

    if not hasattr(expense_date, "isoformat"):
        raise TypeError("expense_date must be a datetime/date object or a string in ISO format.")

    expense = {
        "amount": float(amount),
        "category": category,
        "description": description or "",
        "date": expense_date.isoformat(),
    }

    return expenses_collection.insert_one(expense).inserted_id


def fetch_all_expenses():
    # Defensive check to see if the connection actually works
    if expenses_collection is None:
        raise RuntimeError("Database collection 'expenses_collection' is not initialized. Check your connection setup.")

    return list(expenses_collection.find({}, {"_id": 0}))

