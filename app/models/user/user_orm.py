
# from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserToken(UserBase):
    token: str

class User(UserBase):
    id: int
    character_id: int

    class Config:
        orm_mode = True