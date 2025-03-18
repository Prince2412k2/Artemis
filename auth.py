from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel

from models.models import User, Token, Tokendata


SECRATE_KEY = "10830f099f353ef0a04a8cbac3a40a22dcd9d6c07a8367c739ce346f13795448"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
