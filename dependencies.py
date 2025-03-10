import random
import string
import bcrypt
import logging
import sys
from sqlmodel import Session

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, oauth2
from jose import jwt, JWTError

SECRATE_KEY = "12nfj45647dghs74e7du4e89i4er98ie984we98i4w094oew"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def authenticate_user(username:str,password:str,session:Session):
    user=Session.exec(select(User).where(User.name==username)).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.password):
        return False
    return user

# Configure global logger
def configure_logger(log_level=logging.DEBUG, log_file="app.log"):
    logger = logging.getLogger()  # Get the root logger
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

    # Avoid adding handlers multiple times (when using reload in FastAPI dev mode)
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger




def get_random_id(list_ids: list) -> str:
    while True:
        id = f"{random.choice(string.ascii_uppercase)}{random.randint(0, 9)}{random.randint(0, 9)}"
        if id not in list_ids:
            return id

def main():
    print(get_random_id([]))

if __name__=="__main__":
    main()