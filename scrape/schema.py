from pydantic import BaseModel


class Message(BaseModel):
    message: str


class URL(BaseModel):
    url: str
