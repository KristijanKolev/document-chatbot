from pydantic import BaseModel


class BasicErrorResponse(BaseModel):
    detail: str
