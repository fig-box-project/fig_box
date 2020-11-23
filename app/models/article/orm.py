from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ArticleBase(BaseModel):
    title:           Optional[str] = None
    content:         Optional[str] = None
    description:     Optional[str] = None
    seo_title:       Optional[str] = None
    seo_keywords:    Optional[str] = None
    seo_description: Optional[str] = None
class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    id: int

class Article(ArticleBase):
    id: int
    owner_id: int
    create_date: datetime
    update_date: datetime
    status: int
    class Config:
        orm_mode= True

# class CharaCreate(CharaBase):
