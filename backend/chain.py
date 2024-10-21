import os
from langchain_openai import ChatOpenAI  # Updated to use ChatOpenAI
from langchain.prompts import PromptTemplate
from db import get_recommendation_from_db
from config import OPENAI_API_KEY
import json

# Ensure the OpenAI API key is available
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Make sure it's set in your environment as 'OPENAI_API_KEY'.")

# Initialize the ChatOpenAI model with the API key
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=OPENAI_API_KEY)  # Updated to ChatOpenAI

# Template for the prompt
prompt_template = """
STRICTLY: When user asks to take order, ask for First Name, Middle Name, Last Name, phone number, email and delivery address and do not recommend anything else once user asks to order.

You are a helpful assistant specialized in providing food recommendations and helping with food ordering.

Given the user's query: {user_query}

Restrict your response to food recommendations and assist with placing orders. If the user asks for anything unrelated to food recommendations or ordering, politely decline and suggest a food-related task.

Please recommend only items that are part of a typical restaurant menu like starters, main course, desserts, and drinks.

Respond in a friendly tone.

Strictly always show food items in list form




"""

# Create a prompt template
prompt = PromptTemplate(input_variables=["user_query"], template=prompt_template)

# Use RunnableSequence and pipe the prompt to the Chat LLM
food_recommendation_chain = prompt | llm

import json  # Import the json module

def get_food_recommendation_with_db(user_query):
    try:
        # Get LLM response
        response = food_recommendation_chain.invoke({"user_query": user_query})

        # If the response is an object with additional fields, clean it up
        if hasattr(response, 'content'):
            message = response.content
        elif isinstance(response, dict) and 'content' in response:
            message = response['content']
        else:
            # Fallback in case of unexpected format
            message = str(response)

        # Append actual food items from the database
        if "recommend" in user_query.lower() or "suggest" in user_query.lower():
            db_recommendations = get_recommendation_from_db()
            message += f"\nHere are some items from our menu:\n{db_recommendations}"

        # Create a dictionary for JSON response
        json_response = {
            "user_query": user_query,
            "bot_response": message
        }

        # Convert dictionary to JSON
        return json.dumps(json_response, indent=4)  # Pretty-print the JSON with indentation
    except Exception as e:
        # In case of error, return the error in JSON format
        error_response = {
            "error": str(e)
        }
        return json.dumps(error_response, indent=4)
