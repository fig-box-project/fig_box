
# from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str = "admin"

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str = "admin"
# class UserToken(UserBase):
#     token: str

class UserUpdate(UserBase):
    id: int
    character_id: int

class User(UserBase):
    id: int
    character_id: int

    class Config:
        orm_mode = True