from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ArticleBase(BaseModel):
    title:           Optional[str] = None
    content:         Optional[str] = None
    description:     Optional[str] = None
    category_id:     Optional[int] = None
    seo_title:       Optional[str] = None
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
