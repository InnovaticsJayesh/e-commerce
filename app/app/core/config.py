import os
from typing import Any, Dict, List, Optional, Union
from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings
from pydantic import EmailStr, AnyHttpUrl, HttpUrl, PostgresDsn

load_dotenv(find_dotenv(), verbose=True)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    database_hostname:str = os.getenv("DATABASE_HOSTNAME")
    database_port:str = os.getenv("DATABASE_PORT")
    database_password:str = os.getenv("DATABASE_PASSWORD")
    database_name:str = os.getenv("DATABASE_NAME")
    database_username:str = os.getenv("DATABASE_USERNAME")
    secret_key:str = os.getenv("SECRET_KEY")
    algorithm:str = os.getenv("ALGORITHM")
    access_token_expire_minutes:int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    cookie_name: str = os.getenv("cookie_name")
   
    FIRST_SUPERUSER: str = database_username
    FIRST_SUPERUSER_PASSWORD: str = database_password
 
    DATABASE_URL: str = f"postgresql://{database_username}:{database_password}@{database_hostname}:{database_port}/{database_name}"
 
settings = Settings()