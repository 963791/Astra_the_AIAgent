from pydantic import BaseModel
class ChatRequest(BaisModel):
    message: str