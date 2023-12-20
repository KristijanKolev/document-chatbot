from pydantic import BaseModel

from .chat_prompt import ChatPrompt


class SessionPromptingResponse(BaseModel):
    """Response object for the prompting endpoint"""
    prompt: ChatPrompt
    session_updated: bool
