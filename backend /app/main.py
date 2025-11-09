# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from .agent import run_agent_stream
from .schemas import ChatRequest


app = FastAPI(title="Astra Agent Backend")


# Allow local development origins; lock this down in production
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


@app.get("/")
async def root():
return {"status": "Astra backend is alive 🚀"}


@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
async def event_generator():
async for chunk in run_agent_stream(req.message):
yield chunk
return StreamingResponse(event_generator(), media_type="text/event-stream")