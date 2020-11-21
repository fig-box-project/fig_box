from typing import List, Optional
from pydantic import BaseModel

class ArticleBase(BaseModel):
    title:           Optional[str] = None
    content:         Optional[str] = None
    seo_meta:        Optional[str] = None
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

    class Config:
        orm_mode= True

# class CharaCreate(CharaBase):
