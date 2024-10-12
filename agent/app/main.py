from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain import OpenAI

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_router = APIRouter(prefix="/api")


class PromptRequest(BaseModel):
    prompt: str


class Response(BaseModel):
    response: str
    summary: str


@api_router.post("/generate", response_model=Response)
async def generate_response(request: PromptRequest):

    generated_response = f"Agent response to: {request.prompt}"
    summary = "Summary of the response"

    return {"response": generated_response, "summary": summary}


app.include_router(api_router)
