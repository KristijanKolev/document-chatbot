from sqlalchemy.orm import Session
from fastapi_sso.sso.base import OpenID

from backend.models import User
from backend.schemas.user import UserCreate, UserUpdate
from backend.crud import user as user_crud


class UserService:

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_or_update_sso_user(self, sso_info: OpenID) -> User:

        existing_user = user_crud.get_by_sso_provider(
            db=self.db,
            sso_provider=sso_info.provider,
            sso_id=sso_info.id
        )
        if existing_user is not None:
            # Update modifiable attributes if they have been changed by the SSO provider.
            obj_in = UserUpdate(
                display_name=sso_info.display_name,
                email=sso_info.email,
                picture_url=sso_info.picture
            )

            return user_crud.update(db=self.db, db_obj=existing_user, obj_in=obj_in)
        else:
            # Register new SSO user.
            obj_in = UserCreate(
                sso_id=sso_info.id,
                sso_provider=sso_info.provider,
                display_name=sso_info.display_name,
                email=sso_info.email,
                picture_url=sso_info.picture
            )

            return user_crud.create(db=self.db, obj_in=obj_in)
