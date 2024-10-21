# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load OpenAI API Key and MongoDB URI from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Please set it as an environment variable.")
