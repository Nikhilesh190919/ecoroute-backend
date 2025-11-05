from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import random

app = FastAPI(title="AskEd AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend everywhere for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[dict]
    conversation_id: str

@app.get("/")
async def root():
    return {"message": "AskEd AI API is running", "version": "1.0.0"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    query = req.message.lower()
    if "course" in query:
        reply = "📘 We offer 120+ courses across various departments. You can explore them on the official courses page."
    elif "placement" in query:
        reply = "🎯 Our placement rate is 95%! The Career Center helps with interviews and resume prep."
    else:
        reply = "🤖 I can help with information about courses, placements, and more. Please try again!"
    return ChatResponse(
        response=reply,
        sources=[],
        conversation_id=req.conversation_id or f"conv_{datetime.now().timestamp()}"
    )
