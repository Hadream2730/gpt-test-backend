import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from openai import OpenAIError
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    system: str
    messages: List[Message]
    conversation_id: str = None  # Optional - for continuing conversations

class ChatResponse(BaseModel):
    content: str

class ErrorResponse(BaseModel):
    error: bool = True
    type: str
    message: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],        # Allow all HTTP methods
    allow_headers=["*"],        # Allow all headers
)


@app.get("/")
async def root():
    return {"message": "GPT Test Backend API is running"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        input_messages = [
            {
                "role": m.role,
                "content": m.content
            }
            for m in req.messages
        ]

        # Build the request parameters
        request_params = {
            "model": "gpt-4.1-mini",
            "instructions": req.system,
            "input": input_messages,
        }
        
        # Add conversation_id if provided (for continuing conversations)
        if req.conversation_id:
            request_params["conversation_id"] = req.conversation_id

        response = client.responses.create(**request_params)

        return {
            "error": False,
            "content": response.output_text,
            "conversation_id": getattr(response, 'conversation_id', None)  # Return conversation_id if available
        }

    except OpenAIError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": True,
                "type": "openai_error",
                "message": str(e)
            }
        )
