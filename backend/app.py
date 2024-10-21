import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from chain import get_food_recommendation_with_db  # Assuming this function is in chain.py
import json  # Add this import

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/recommend', methods=['POST'])
def recommend_food():
    data = request.json
    user_query = data.get('query', '')

    # Use the user's IP as a basic session ID for now, or a simple static session ID for testing
    session_id = request.remote_addr or 'session_1'

    # Get recommendation response from the chatbot logic
    response_json = get_food_recommendation_with_db(user_query, session_id)

    # Return the response as JSON
    return jsonify(json.loads(response_json))  # Convert JSON string to Python dict and return it

if __name__ == '__main__':
    app.run(debug=True)
