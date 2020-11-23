from typing import List, Optional
from pydantic import BaseModel

class CharaBases(BaseModel):
    name: str
    can_edit_auth: bool
    can_edit_tree: bool
    can_edit_article: bool
    can_edit_all_article: bool
    can_edit_character: bool

class CharacterCreate(CharaBases):
    pass

class CharaUpdate(CharaBases):
    pass

class Chara(CharaBases):
    id: int

    class Config:
        orm_mode= True

# class CharaCreate(CharaBase):
