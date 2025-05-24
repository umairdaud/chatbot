# Loading the environment variables from .env file
from dotenv import load_dotenv
import rich  
import os  

# Loads the contents from .env file
load_dotenv()

# Getting the configuration values from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")         
gemini_api_url = os.getenv("GEMINI_API_URL")         
gemini_api_model = os.getenv("GEMINI_API_MODEL")     

# Check if any of the required environment variables are missing
if not gemini_api_key or not gemini_api_url or not gemini_api_model:
    print("Please set the environment variables GEMINI_API_KEY, GEMINI_API_URL, and GEMINI_API_MODEL.")
    exit(1)

# Defining a class
class Secrets:
    def __init__(self):
        # Assigning the environment variables to instance attributes
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_api_url = os.getenv("GEMINI_API_URL")
        self.gemini_api_model = os.getenv("GEMINI_API_MODEL")

        