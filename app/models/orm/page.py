from typing import Optional
from pydantic import BaseModel


class Page(BaseModel):
    link: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    seo_title: Optional[str] = None
    seo_keywords: Optional[str] = None
    seo_description: Optional[str] = None
