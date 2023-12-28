from typing import Annotated
from datetime import datetime, timedelta

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, Response
from fastapi_sso.sso.github import GithubSSO
from jose import JWTError, jwt

from backend import schemas
from backend.config.settings import settings
from backend.service import UserService
from backend.security.util import create_access_token
from ..deps import get_user_service, oauth2_scheme


router = APIRouter()

github_sso = GithubSSO(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_SECRET,
    redirect_uri="http://localhost:8000/api/auth/github/callback",
    allow_insecure_http=True
)


@router.get("/github/login")
async def github_auth_init():
    """Initialize auth and redirect"""
    with github_sso:
        return await github_sso.get_login_redirect()


@router.get("/github/callback")
async def github_auth_callback(
        request: Request,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Verify login"""
    with github_sso:
        github_user = await github_sso.verify_and_process(request)
        user = user_service.create_or_update_sso_user(github_user)

        expires_delta = timedelta(minutes=settings.JWT_EXPIRATION_DELTA)
        expires_seconds = settings.JWT_EXPIRATION_DELTA * 60

        token_payload = schemas.TokenData(user_id=user.id)
        access_token = create_access_token(token_payload.model_dump(), expires_delta=expires_delta)

        response = RedirectResponse(url=settings.OAUTH_SUCCESS_REDIRECT_URL)
        response.set_cookie(key="jwt", value=access_token, max_age=expires_seconds)
        return response


@router.get("/refresh-token", response_model=schemas.Token)
def refresh_token(token: Annotated[str, Depends(oauth2_scheme)], response: Response):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    expires_delta = timedelta(minutes=settings.JWT_EXPIRATION_DELTA)
    expires_seconds = settings.JWT_EXPIRATION_DELTA * 60
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        token_data = schemas.TokenData.model_validate(payload, strict=False)
        if token_data.user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    new_token = create_access_token(token_data.model_dump(), expires_delta=expires_delta)
    response.set_cookie(key="jwt", value=new_token, max_age=expires_seconds)
    return schemas.Token(access_token=new_token, token_type='bearer')

