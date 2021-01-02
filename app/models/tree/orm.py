
from typing import List, Optional
from pydantic import BaseModel

class LeafBase(BaseModel):
    name: str = ""
    description: str = ""

class LeafCreate(LeafBase):
    def getMap(self):
        ma = self.__dict__
        ma['children'] =[]
        return ma

class Update(LeafBase):
    id: int = 0
    link:                Optional[str] = None
    content:             Optional[str] = None
    status:bool = True
    seo_title:           Optional[str] = None
    seo_keywords:        Optional[str] = None
    seo_description:     Optional[str] = None
    image:               Optional[str] = None
    def get_update_map(self,old_data:dict):
        if self.name != "":
            old_data["name"] = self.name
        if self.description != "":
            old_data["description"] = self.description
        return old_data

# 返回时使用?
class CatecoryData(BaseModel):
    link: Optional[str] = None
    name: str
    content: str

    status:bool = True

    image:str
    description: str
    seo_title: str
    seo_keywords: str
    seo_description: str
