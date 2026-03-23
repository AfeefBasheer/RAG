from app.auth.auth_schema import UserBody
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
import os
from dotenv import load_dotenv

load_dotenv()

JWT_KEY = os.getenv("JWT_SECRET")
JWT_LIFETIME = os.getenv("JWT_EXPIRY_MINUTES")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user_payload = check_token_validity(token)
        user = UserBody(
            user_id=user_payload["user_id"],
            tenant_id=user_payload["tenant_id"],
            user_role=user_payload["role"],
        )
        return user
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))


def check_token_validity(token):
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
