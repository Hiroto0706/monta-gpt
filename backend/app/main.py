import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from api import router as api_router
import utilities.config as config

# 全てのモデルのインポート
from infrastructure.database.models import *

logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.ALLOW_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api")