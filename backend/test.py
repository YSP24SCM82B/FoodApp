import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the client directly with the API key
client = openai.Client(api_key=api_key)

try:
    # Use client.chat.completions.create() in the new SDK format
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for a food ordering app."},
            {"role": "user", "content": "Hello! Can you confirm if you're working?"}
        ],
        max_tokens=50,
        temperature=0.7
    )

    # Access the generated message content
    bot_response = response.choices[0].message.content.strip()
    print(bot_response)
except Exception as e:
    print("Error:", e)
