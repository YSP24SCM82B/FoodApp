from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from chain import get_food_recommendation_with_db
import json  # Import the json module

app = Flask(__name__)

# Enable CORS and allow requests from 'http://localhost:3000'
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api/recommend', methods=['POST'])
def recommend_food():
    data = request.json
    user_query = data.get('query', '')

    # Get recommendation response from the chatbot logic
    response_json = get_food_recommendation_with_db(user_query)

    # Return the response as JSON
    return jsonify(json.loads(response_json))  # Convert JSON string to Python dict and return it

if __name__ == '__main__':
    app.run(debug=True)
