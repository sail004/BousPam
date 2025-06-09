import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

def get_auth_data():
    return {"secret_key": SECRET_KEY, "algorithm": ALGORITHM}
