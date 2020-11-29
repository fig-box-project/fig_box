from typing import List, Optional
from pydantic import BaseModel

class CharaBases(BaseModel):
    """
        name: 角色名称 \n
        can_edit_auth: 能否编辑其它用户的资料 \n
        can_edit_tree: 能否编辑分类 \n
        can_edit_article: 能否编辑自己的文章\n
        can_edit_all_article: 能否编辑所有的文章\n
        can_edit_character: 能否编辑角色\n
    """
    name: str
    can_edit_auth: bool = False
    can_edit_tree: bool = False
    can_edit_article: bool = True
    can_edit_all_article: bool = False
    can_edit_character: bool = False

class CharacterCreate(CharaBases):
    pass

class CharaUpdate(CharaBases):
    pass

class Chara(CharaBases):
    id: int

    class Config:
        orm_mode= True

# class CharaCreate(CharaBase):
