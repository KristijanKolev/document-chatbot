from pydantic import BaseModel


class TokenData(BaseModel):
    user_id: int


class Token(BaseModel):
    access_token: str
    token_type: str
