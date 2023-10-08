from pydantic import BaseModel


class UserBase(BaseModel):
    display_name: str
    email: str
    picture_url: str


class User(UserBase):
    sso_provider: str
    sso_id: str
    id: int

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    sso_provider: str
    sso_id: str


class UserUpdate(UserBase):
    pass
