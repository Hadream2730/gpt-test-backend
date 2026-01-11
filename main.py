import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

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

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
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
            model="gpt-4.1-mini",
            input=input_messages,
            temperature=0.7
        )

        return ChatResponse(content=response.output_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
