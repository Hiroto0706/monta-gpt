from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import utilities.config as config
from api import router as api_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.ALLOW_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api")


@app.get("/")
def hello_world():
    return {"message": "Hello world from agent app. Ask me anything!"}
