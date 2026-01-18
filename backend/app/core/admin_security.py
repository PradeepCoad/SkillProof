from datetime import datetime, timedelta
from jose import jwt 

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "admin_super_secret"
ALGORITHM = "HS256"
ADMIN_TOKEN_EXPIRE_MINUTES = 60


def create_admin_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ADMIN_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)