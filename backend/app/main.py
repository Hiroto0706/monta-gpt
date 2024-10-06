from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api import router as api_router
import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENV", "dev")
env_file = f".env.{env}"
load_dotenv(env_file, override=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api")
