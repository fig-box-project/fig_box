
# from typing import List, Optional
from pydantic import BaseModel

class CharaBase(BaseModel):
    pass

class CharaCreate(CharaBase):
    name: str = "superman"
    auths: list
    description: str = "默认说明"

class CharaOne(CharaBase):
    name: str = "superman"
    auth: str = "abc"


class Chara(CharaCreate):
    class Config:
        orm_mode = True