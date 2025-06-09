import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
API_KEY = os.getenv('API_KEY')

def get_auth_data():
    return {"secret_key": SECRET_KEY, "algorithm": ALGORITHM}

def get_api_key():
    return API_KEY
