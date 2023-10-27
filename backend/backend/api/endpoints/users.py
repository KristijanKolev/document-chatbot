from typing import Annotated

from fastapi import APIRouter, Depends

from backend.models.user import User
from backend.schemas import User as UserSchema
from ..deps import get_current_user


router = APIRouter()


@router.get("/me", response_model=UserSchema)
def get_current_authenticated_user(user: Annotated[User, Depends(get_current_user)]):
    return user
