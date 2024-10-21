import os
from langchain_openai import ChatOpenAI  # Updated to use ChatOpenAI
from langchain.prompts import PromptTemplate
from db import get_recommendation_from_db
from config import OPENAI_API_KEY
import json
import random  # For generating the order ID
from pymongo import MongoClient  # Importing MongoDB client

# Ensure the OpenAI API key is available
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Make sure it's set in your environment as 'OPENAI_API_KEY'.")

# Initialize the ChatOpenAI model with the API key
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=OPENAI_API_KEY)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI if hosted elsewhere
db = client['Foodservices']
orders_collection = db['Orders']

# Template for the prompt
prompt_template = """
You are a helpful assistant specialized in providing food recommendations and assisting with food ordering.

Given the user's query: {user_query}

Restrict your response to food recommendations and assist with placing orders. If the user asks for anything unrelated to food recommendations or ordering, politely decline and suggest a food-related task.

Please recommend only items that are part of a typical restaurant menu like starters, main course, desserts, and drinks.

Respond in a friendly tone.

Strictly always show food items in list form.

STRICTLY: When the user asks to take an order, ask for First Name, Middle Name, Last Name, phone number, email, and delivery address. Do not recommend anything else once the user asks to place an order.

STRICTLY: Generate a random Order ID once all details are provided AND display the message "Order placed successfully. Your Order ID is {{OrderID}}."
"""

# Create a prompt template
prompt = PromptTemplate(input_variables=["user_query"], template=prompt_template)

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


def get_food_recommendation_with_db(user_query, session_id):
    try:
        # Check if the user is already in an order session
        if session_id in order_sessions and order_sessions[session_id]['collecting_order']:
            # We're in the process of collecting order details
            order_details = order_sessions[session_id]
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
                    "bot_response": "Almost done! Finally, please provide your delivery address."
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
                "bot_response": "Sure! Let's start with your Name."
            }, indent=4)

        # Generate the prompt using the user's query
        formatted_prompt = prompt.format(user_query=user_query)

        # Get the LLM response
        response = llm.generate([formatted_prompt])  # Use generate instead of run

        # Extract the message from the response
        if response and response.generations and response.generations[0]:
            message = response.generations[0][0].text
        else:
            message = "Sorry, I couldn't process your request."

        # Append actual food items from the database if the user is asking for recommendations
        if "recommend" in user_query.lower() or "suggest" in user_query.lower():
            db_recommendations = get_recommendation_from_db()
            message += f"\nHere are some items from our menu:\n{db_recommendations}"

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
