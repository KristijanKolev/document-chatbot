from sqlalchemy.orm import Session

from backend.schemas.user import UserCreate, UserUpdate
from backend.models.user import User
from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_sso_provider(self, db: Session, sso_provider: str, sso_id: str) -> User | None:
        return db.query(self.model).filter(
            User.sso_provider == sso_provider and
            User.sso_id == sso_id
        ).first()


user = CRUDUser(User)
