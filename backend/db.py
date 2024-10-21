# db.py
from pymongo import MongoClient
from config import MONGO_URI

# Connect to MongoDB using the URI from the config or environment variable
client = MongoClient(MONGO_URI)
db = client['Foodservices']
collection = db['Fooditems']

def get_recommendation_from_db():
    # Retrieve food items from the Fooditems collection
    food_items = list(collection.find({}, {'name': 1, 'description': 1, '_id': 0}))
    recommendations = "\n".join([f"{item['name']}: {item['description']}" for item in food_items])
    return recommendations
