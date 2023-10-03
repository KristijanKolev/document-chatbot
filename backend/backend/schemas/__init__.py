from .chat_session import ChatSessionCreate, ChatSession, ChatSessionUpdate
from .chat_prompt import ChatPrompt, ChatPromptCreate, ChatPromptIn, ChatPromptSimple

# Update the references that are as strings
ChatSession.model_rebuild()
ChatPrompt.model_rebuild()
