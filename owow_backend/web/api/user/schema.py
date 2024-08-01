from pydantic import BaseModel


class UserRequestSchema(BaseModel):
    password: str
    username: str
