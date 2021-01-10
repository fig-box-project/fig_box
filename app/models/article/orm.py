from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import Query

class ArticleBase(BaseModel):
    title:           str = Query(...,min_length=1) # 不能为空的意思
    content:         str = Query(...,min_length=1)
    description:     Optional[str] = None
    category_id:     Optional[int] = None
    image:           Optional[str] = None
    seo_title:       str = Query(...,min_length=1)
    seo_keywords:    Optional[str] = None
    seo_description: Optional[str] = None
class ArticleCreate(ArticleBase):
    status: int
    is_release: bool = False
    can_search: bool = True

class ArticleUpdate(ArticleBase):
    id: int
    link: Optional[str] = None

class ArticleRelease(BaseModel):
    id: int
    can_search: bool = True

class Article(ArticleBase):
    id: int
    link: str
    owner_id: int
    create_date: datetime
    update_date: datetime
    status: int
    class Config:
        orm_mode= True

# class CharaCreate(CharaBase):
