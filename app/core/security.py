from fastapi import HTTPException
def authorize(authorization):
 from .config import settings
 if authorization != f'Bearer {settings.auth_token}': raise HTTPException(status_code=401,detail='Unauthorized')
