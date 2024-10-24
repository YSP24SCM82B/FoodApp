# import os
# from langchain_openai import ChatOpenAI  # Updated to use ChatOpenAI
# from langchain.prompts import PromptTemplate
# from config import OPENAI_API_KEY
# import json
# import random  # For generating the order ID
# from pymongo import MongoClient  # Importing MongoDB client
#
# # Ensure the OpenAI API key is available
# if not OPENAI_API_KEY:
#     raise ValueError("OpenAI API key not found. Make sure it's set in your environment as 'OPENAI_API_KEY'.")
#
# # Initialize the ChatOpenAI model with the API key
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=OPENAI_API_KEY)
#
# # MongoDB connection
# client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI if hosted elsewhere
# db = client['Foodservices']
# fooditems_collection = db['Fooditems']
# orders_collection = db['Orders']
#
# # Template for the prompt
# prompt_template = """
# You are a helpful assistant specialized in providing food recommendations and assisting with food ordering.
#
# Given the user's query: {user_query}
#
# Here are the available food items:
# {food_items}
#
# Respond with a list of food recommendations based on the user's query, but strictly use the food items provided above.
# """
#
# # Create a prompt template
# prompt = PromptTemplate(input_variables=["user_query", "food_items"], template=prompt_template)
#
# # In-memory storage for order details (this would normally be a database)
# order_sessions = {}
#
# def generate_order_id():
#     """Function to generate a random Order ID"""
#     return f"#{random.randint(10000, 99999)}"
#
# def store_order_to_db(order_details):
#     """Function to store the order details to MongoDB"""
#     try:
#         order_id = generate_order_id()
#         order_details['order_id'] = order_id
#         # Insert the order into the Orders collection
#         orders_collection.insert_one(order_details)
#         return order_id
#     except Exception as e:
#         raise Exception(f"Failed to store order: {str(e)}")
#
# def get_recommendation_from_db():
#     """Function to get food recommendations from MongoDB"""
#     try:
#         # Query MongoDB for food items
#         food_items = fooditems_collection.find({}, {'name': 1, 'description': 1, 'cuisine': 1, 'price': 1, 'spiceLevel': 1})
#         recommendations = []
#         for item in food_items:
#             recommendations.append(f"{item['name']} - {item['description']} (Cuisine: {item['cuisine']}, Price: ${item['price']}, Spice Level: {item['spiceLevel']})")
#         return "\n".join(recommendations)
#     except Exception as e:
#         return f"Error fetching recommendations: {str(e)}"
#
# def get_food_recommendation_with_db(user_query, session_id):
#     try:
#         # Check if the user is already in an order session
#         if session_id in order_sessions and order_sessions[session_id]['collecting_order']:
#             # We're in the process of collecting order details
#             order_details = order_sessions[session_id]
#
#             if 'fooditem_name' not in order_details:
#                 order_sessions[session_id]['fooditem_name'] = user_query
#                 return json.dumps({
#                     "user_query": user_query,
#                     "bot_response": "Great! Let's continue. Please provide your first name."
#                 }, indent=4)
#
#             if 'Name' not in order_details:
#                 order_sessions[session_id]['Name'] = user_query
#                 return json.dumps({
#                     "user_query": user_query,
#                     "bot_response": "Great! Now, please provide your phone number."
#                 }, indent=4)
#             elif 'phone_number' not in order_details:
#                 order_sessions[session_id]['phone_number'] = user_query
#                 return json.dumps({
#                     "user_query": user_query,
#                     "bot_response": "Thanks! Now, please provide your email address."
#                 }, indent=4)
#             elif 'email' not in order_details:
#                 order_sessions[session_id]['email'] = user_query
#                 return json.dumps({
#                     "user_query": user_query,
#                     "bot_response": "Great! How many portions or quantity of food would you like to order?"
#                 }, indent=4)
#             elif 'quantity' not in order_details:
#                 order_sessions[session_id]['quantity'] = user_query  # Storing the quantity
#                 return json.dumps({
#                     "user_query": user_query,
#                     "bot_response": "Almost done! Please provide your delivery address."
#                 }, indent=4)
#             elif 'delivery_address' not in order_details:
#                 # Once delivery address is provided, generate order ID and store in DB
#                 order_sessions[session_id]['delivery_address'] = user_query
#                 # Store order to MongoDB
#                 order_id = store_order_to_db(order_sessions[session_id])
#                 del order_sessions[session_id]  # Clear the session after storing
#                 return json.dumps({
#                     "user_query": user_query,
#                     "bot_response": f"Order placed successfully. Your Order ID is {order_id}. Thank you for ordering with us!"
#                 }, indent=4)
#
#         # If user is placing an order, start collecting details
#         if "place an order for" in user_query.lower() or "order" in user_query.lower():
#             order_sessions[session_id] = {'collecting_order': True}
#             return json.dumps({
#                 "user_query": user_query,
#                 "bot_response": "Please specify the food item you'd like to order."
#             }, indent=4)
#
#         # Get food recommendations from MongoDB
#         db_recommendations = get_recommendation_from_db()
#
#         # Generate the prompt using the user's query and the fetched food items
#         formatted_prompt = prompt.format(user_query=user_query, food_items=db_recommendations)
#
#         # Get the LLM response
#         response = llm.generate([formatted_prompt])
#
#         # Extract the message from the response
#         if response and response.generations and response.generations[0]:
#             message = response.generations[0][0].text
#         else:
#             message = "Sorry, I couldn't process your request."
#
#         # Create a dictionary for the JSON response
#         json_response = {
#             "user_query": user_query,
#             "bot_response": message
#         }
#
#         # Convert the dictionary to a JSON string with pretty-printing
#         return json.dumps(json_response, indent=4)
#
#     except Exception as e:
#         # In case of an error, return the error in JSON format
#         error_response = {
#             "error": str(e)
#         }
#         return json.dumps(error_response, indent=4)




import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config import OPENAI_API_KEY
import json
import random
from pymongo import MongoClient

# Ensure the OpenAI API key is available
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Make sure it's set in your environment as 'OPENAI_API_KEY'.")

# Initialize the ChatOpenAI model with the API key
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=OPENAI_API_KEY)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI if hosted elsewhere
db = client['Foodservices']
fooditems_collection = db['Fooditems']
orders_collection = db['Orders']

# Template for the prompt
prompt_template = """
You are a helpful assistant specialized in providing food recommendations and assisting with food ordering.

Given the user's query: {user_query}

Here are the available food items:
{food_items}

Respond with a list of food recommendations based on the user's query, but strictly use the food items provided above.
"""

# Create a prompt template
prompt = PromptTemplate(input_variables=["user_query", "food_items"], template=prompt_template)

# In-memory storage for order details (this would normally be a database)
order_sessions = {}

def generate_order_id():
    """Function to generate a random Order ID"""
    return f"#{random.randint(10000, 99999)}"

def store_order_to_db(order_details):
    """Function to store the order details to MongoDB"""
    try:
        order_id = generate_order_id()
        order_details['order_id'] = order_id
        # Insert the order into the Orders collection
        orders_collection.insert_one(order_details)
        return order_id
    except Exception as e:
        raise Exception(f"Failed to store order: {str(e)}")

def get_recommendation_from_db():
    """Function to get food recommendations from MongoDB"""
    try:
        # Query MongoDB for food items, including imageUrl
        food_items = fooditems_collection.find({}, {'name': 1, 'description': 1, 'cuisine': 1, 'price': 1, 'spiceLevel': 1, 'imageUrl': 1})
        recommendations = []
        for item in food_items:
            recommendations.append({
                "name": item['name'],
                "description": item['description'],
                "cuisine": item['cuisine'],
                "price": item['price'],
                "spiceLevel": item['spiceLevel'],
                "imageUrl": item.get('imageUrl', '')  # Ensure imageUrl is included
            })
        return recommendations
    except Exception as e:
        return f"Error fetching recommendations: {str(e)}"


def get_food_recommendation_with_db(user_query, session_id):
    try:
        # Check if the user is already in an order session
        if session_id in order_sessions and order_sessions[session_id]['collecting_order']:
            # We're in the process of collecting order details
            order_details = order_sessions[session_id]

            if 'fooditem_name' not in order_details:
                order_sessions[session_id]['fooditem_name'] = user_query
                return json.dumps({
                    "user_query": user_query,
                    "bot_response": "Great! Let's continue. Please provide your first name."
                }, indent=4)

            if 'Name' not in order_details:
                order_sessions[session_id]['Name'] = user_query
                return json.dumps({
                    "user_query": user_query,
                    "bot_response": "Great! Now, please provide your phone number."
                }, indent=4)
            elif 'phone_number' not in order_details:
                order_sessions[session_id]['phone_number'] = user_query
                return json.dumps({
                    "user_query": user_query,
                    "bot_response": "Thanks! Now, please provide your email address."
                }, indent=4)
            elif 'email' not in order_details:
                order_sessions[session_id]['email'] = user_query
                return json.dumps({
                    "user_query": user_query,
                    "bot_response": "Great! How many portions or quantity of food would you like to order?"
                }, indent=4)
            elif 'quantity' not in order_details:
                order_sessions[session_id]['quantity'] = user_query  # Storing the quantity
                return json.dumps({
                    "user_query": user_query,
                    "bot_response": "Almost done! Please provide your delivery address."
                }, indent=4)
            elif 'delivery_address' not in order_details:
                # Once delivery address is provided, generate order ID and store in DB
                order_sessions[session_id]['delivery_address'] = user_query
                # Store order to MongoDB
                order_id = store_order_to_db(order_sessions[session_id])
                del order_sessions[session_id]  # Clear the session after storing
                return json.dumps({
                    "user_query": user_query,
                    "bot_response": f"Order placed successfully. Your Order ID is {order_id}. Thank you for ordering with us!"
                }, indent=4)

        # If user is placing an order, start collecting details
        if "place an order for" in user_query.lower() or "order" in user_query.lower():
            order_sessions[session_id] = {'collecting_order': True}
            return json.dumps({
                "user_query": user_query,
                "bot_response": "Please specify the food item you'd like to order."
            }, indent=4)

        # Get food recommendations from MongoDB
        db_recommendations = get_recommendation_from_db()

        # Generate the prompt using the user's query and the fetched food items
        formatted_prompt = prompt.format(user_query=user_query, food_items=db_recommendations)

        # Get the LLM response
        response = llm.generate([formatted_prompt])

        # Extract the message from the response
        if response and response.generations and response.generations[0]:
            message = response.generations[0][0].text
        else:
            message = "Sorry, I couldn't process your request."

        # Create a dictionary for the JSON response
        json_response = {
            "user_query": user_query,
            "bot_response": message
        }

        # Convert the dictionary to a JSON string with pretty-printing
        return json.dumps(json_response, indent=4)

    except Exception as e:
        # In case of an error, return the error in JSON format
        error_response = {
            "error": str(e)
        }
        return json.dumps(error_response, indent=4)
