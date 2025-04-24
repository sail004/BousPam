SECRET_KEY='gV64m9aIzFG4qpgVphvQbPQrtAO0nM-7YwwOvu0XPt5KJOjAy4AfgLkqJXYEt'
ALGORITHM='HS256'






def get_auth_data():
    return {"secret_key": SECRET_KEY, "algorithm": ALGORITHM}