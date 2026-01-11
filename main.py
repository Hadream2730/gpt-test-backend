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
    print(req)
    try:
        input_messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": req.system}]
            }
        ]

        for m in req.messages:
            input_messages.append({
                "role": m.role,
                "content": [{"type": "text", "text": m.content}]
            })

        response = client.responses.create(
            model="gpt-4.1",
            input="Tell me a three sentence bedtime story about a unicorn.",
            # temperature=0.7
        )

        return {
            "error": False,
            "content": response.output
        }

    # ---- OpenAI-specific errors ----
    except OpenAIError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": True,
                "type": "openai_error",
                "message": str(e)
            }
        )

    # ---- Any other backend error ----
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": True,
                "type": "server_error",
                "message": "Internal server error"
            }
        )
