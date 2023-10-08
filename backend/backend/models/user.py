from sqlalchemy import Column, Integer, String, UniqueConstraint

from ..db.database import Base


class User(Base):
    """Model for SSO users."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    sso_provider = Column(String(20), nullable=False)
    sso_id = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    picture_url = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint(id, sso_id, name="unique_sso_user"),
    )

