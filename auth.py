from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel

from models.models import User, Token, Tokendata



SECRATE_KEY = "12nfj45647dghs74e7du4e89i4er98ie984we98i4w094oew"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
