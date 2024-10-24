from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['Foodservices']
fooditems_collection = db['Fooditems']

def get_recommendation_from_db():
    """Function to get food recommendations from MongoDB"""
    try:
        # Query MongoDB for food items
        food_items = fooditems_collection.find({}, {'name': 1, 'description': 1, 'cuisine': 1, 'price': 1, 'spiceLevel': 1})
        recommendations = []
        for item in food_items:
            recommendations.append(f"{item['name']} - {item['description']} (Cuisine: {item['cuisine']}, Price: ${item['price']}, Spice Level: {item['spiceLevel']})")
        return "\n".join(recommendations)
    except Exception as e:
        return f"Error fetching recommendations: {str(e)}"

# Testing the function
if __name__ == "__main__":
    recommendations = get_recommendation_from_db()
    print(recommendations)
