from fastapi import FastAPI
from pydantic import BaseModel
from langchain import OpenAI

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str


class Response(BaseModel):
    response: str
    summary: str


@app.post("/generate", response_model=Response)
async def generate_response(request: PromptRequest):

    generated_response = f"Agent response to: {request.prompt}"
    summary = "Summary of the response"

    return {"response": generated_response, "summary": summary}
