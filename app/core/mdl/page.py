from datetime import datetime

from starlette.requests import Request

from typing import Optional
from sqlalchemy import Column, String
from pydantic import BaseModel
from fastapi import Query
from . import DateCUMdl
from ..tools import Tools


class PageMdl(DateCUMdl):
    __abstract__ = True

    # unique要改True, 暂时无用
    link = Column(String, unique=False, index=True)
    title = Column(String(64), index=True)
    content = Column(String)

    image = Column(String)
    description = Column(String(200))
    seo_title = Column(String(40))
    seo_keywords = Column(String(256))
    seo_description = Column(String(400))

    def reset_image_url(self, request: Request):
        """将image重设为完整网址"""
        # TODO: 上线后改为https
        self.image = Tools.get_assets_url(self.image, request)


class PageOrm(BaseModel):
    link: Optional[str] = None
    title: str = Query(..., min_length=1)  # 不能为空的意思
    content: str = Query(..., min_length=1)
    image: Optional[str] = None
    description: Optional[str] = None
    seo_title: str = Query(..., min_length=1)
    seo_keywords: Optional[str] = None
    seo_description: Optional[str] = None

    def dict_when_create(self):
        now = datetime.now()
        rt = self.dict()
        rt['create_date'] = now
        rt['update_date'] = now
        return rt

    def dict_when_update(self):
        now = datetime.now()
        rt = self.dict()
        rt['update_date'] = now
        return rt
