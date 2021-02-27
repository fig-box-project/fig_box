
# from typing import List, Optional
from pydantic import BaseModel

class CharaCreate(BaseModel):
    name: str = "superman"
    auths: list
    description: str

class Chara(CharaCreate):
    class Config:
        orm_mode = True