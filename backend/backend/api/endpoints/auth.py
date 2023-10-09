from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi_sso.sso.github import GithubSSO

from backend import schemas
from backend.config.settings import settings
from backend.service import UserService
from backend.security.util import create_access_token
from ..deps import get_user_service


router = APIRouter()

github_sso = GithubSSO(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_SECRET,
    redirect_uri="http://localhost:8000/auth/github/callback",
    allow_insecure_http=True
)


@router.get("/github/login")
async def github_auth_init():
    """Initialize auth and redirect"""
    with github_sso:
        return await github_sso.get_login_redirect()


@router.get("/github/callback", response_model=schemas.Token)
async def github_auth_callback(
        request: Request,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Verify login"""
    with github_sso:
        github_user = await github_sso.verify_and_process(request)
        user = user_service.create_or_update_sso_user(github_user)

        token_payload = schemas.TokenData(user_id=user.id)
        access_token = create_access_token(token_payload.model_dump())

        return schemas.Token(access_token=access_token, token_type='bearer')
