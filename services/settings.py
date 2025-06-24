import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

load_dotenv()

SECRET_KEY = Ed25519PrivateKey.generate()
ALGORITHM = os.getenv('ALGORITHM')
API_KEY = os.getenv('API_KEY')

def get_auth_data():
    return {"secret_key": SECRET_KEY, "algorithm": ALGORITHM}

def get_api_key():
    return API_KEY
