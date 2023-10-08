from fastapi import FastAPI

from .endpoints import chat_sessions, auth


app = FastAPI()

app.include_router(
    chat_sessions.router,
    prefix='/sessions'
)
app.include_router(
    auth.router,
    prefix='/auth'
)
