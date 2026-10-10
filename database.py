import os
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
        db = client["expense_tracker"] # Your database name
        expenses_collection = db["expenses"] # Your collection name
        print("Connected to MongoDB successfully.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

# 3. Ensure this runs when the module is imported
init_db()

def fetch_all_expenses():
    # Defensive check to see if the connection actually works
    if expenses_collection is None:
        raise RuntimeError("Database collection 'expenses_collection' is not initialized. Check your connection setup.")
        
    return list(expenses_collection.find())

