from app.auth.auth_repository import get_user_by_email
from app.auth.auth_schema import UserLoginRequestSchema, UserRecord
from bcrypt import checkpw
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

JWT_KEY = os.getenv("JWT_SECRET")
JWT_LIFETIME = os.getenv("JWT_EXPIRY_MINUTES")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def login_user(request_user: UserLoginRequestSchema):
    user_data = get_user_by_email(request_user.email)

    if not user_data:
        raise ValueError("User not found")
    user = UserRecord(
        user_id=user_data["user_id"],
        password_hash=user_data["password_hash"],
        tenant_id=user_data["tenant_id"],
        user_role="user",
    )
    if not checkpw(
        request_user.password.encode("utf-8"), user.password_hash.encode("utf-8")
    ):
        raise ValueError("Invalid Password")
    token = create_new_token(user)
    return token


def create_new_token(user):
    user_payload = {
        "user_id": str(user.user_id),
        "tenant_id": str(user.tenant_id),
        "role": "user",
        "exp": datetime.utcnow() + timedelta(minutes=int(JWT_LIFETIME)),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload=user_payload, key=JWT_KEY, algorithm=JWT_ALGORITHM)
    print(token)
    return token

