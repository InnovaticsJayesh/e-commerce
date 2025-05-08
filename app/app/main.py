import uuid
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
 
import sys
 
sys.path.append('../')
 
from app.api.api_v1.api import api_router
 
app = FastAPI()
get_secret_key = uuid.uuid4()

app.add_middleware(SessionMiddleware, secret_key= get_secret_key)
 
origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000"   # sometimes this too
]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
app.include_router(api_router)