import os
from dotenv import load_dotenv

load_dotenv()
MISTRAL_API_KEY = os.environ.get('MISTRAL_API_KEY')
