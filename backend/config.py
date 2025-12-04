import os
from dotenv import load_dotenv

load_dotenv()

APPLE_ID = os.getenv('APPLE_ID')
APPLE_PASSWORD = os.getenv('APPLE_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')