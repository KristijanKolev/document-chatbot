from fastapi import FastAPI, APIRouter

from .endpoints import chat_sessions, auth, users


app = FastAPI()

main_api_router = APIRouter()

main_api_router.include_router(
    chat_sessions.router,
    prefix='/sessions'
)
main_api_router.include_router(
    auth.router,
    prefix='/auth'
)
main_api_router.include_router(
    users.router,
    prefix='/users'
)

app.include_router(main_api_router, prefix='/api')
