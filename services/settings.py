import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives.serialization import load_pem_private_key

load_dotenv()
pem_bytes = os.getenv('SECRET_KEY_PEM')
pem = f"""-----BEGIN PRIVATE KEY-----
{pem_bytes}
-----END PRIVATE KEY-----"""
SECRET_KEY = load_pem_private_key(pem.encode('utf-8'), password=None)
ALGORITHM = os.getenv('ALGORITHM')
API_KEY = os.getenv('API_KEY')

def get_auth_data():
    return {"secret_key": SECRET_KEY, "algorithm": ALGORITHM}

def get_api_key():
    return API_KEY
