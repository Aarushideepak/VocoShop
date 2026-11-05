import logging
logging.getLogger("gnani").setLevel(logging.WARNING)
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Gnani API key
api_key = os.getenv("GNANI_API_KEY")


if api_key:
    print("Gnani API key loaded successfully!")
else:
    print("API key not found. Check your .env file.")