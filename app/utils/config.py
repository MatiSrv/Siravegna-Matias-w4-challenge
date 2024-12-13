from dotenv import load_dotenv
import os


# cargar el api key de cohere
load_dotenv()  # Load .env file
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
