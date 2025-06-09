from fastapi import FastAPI, Depends, HTTPException, Header
from .settings import get_api_key


async def verify_api_key(api_key: str = Header(..., alias="X-API-Key")):
    valid_api_key = get_api_key()

    if api_key != valid_api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return True
