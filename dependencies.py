import random
import string
import logging
import sys
from sqlmodel import Session, select
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from models.models import User

SECRET_KEY = "12nfj45647dghs74e7du4e89i4er98ie984we98i4w094oew"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/user/login")


def authenticate_user(username: str, password: str, session: Session):
    user = session.exec(select(User).where(User.name == username)).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=404, detail="Invalid JWT token")
        return None


# Configure global logger
def configure_logger(log_level=logging.DEBUG, log_file="app.log"):
    logging.getLogger('passlib').setLevel(logging.ERROR)
    
    logger = logging.getLogger()  # Root logger

    if not logger.hasHandlers():  # Only add handlers if none exist
        logger.setLevel(log_level)

        # Formatter for logs
        formatter = logging.Formatter(
            "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_random_id(list_ids: list) -> str:
    while True:
        id = f"{random.choice(string.ascii_uppercase)}{random.randint(0, 9)}{random.randint(0, 9)}"
        if id not in list_ids:
            return id


def main():
    print(get_random_id([]))


if __name__ == "__main__":
    main()
