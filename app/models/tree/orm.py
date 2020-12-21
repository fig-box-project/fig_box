
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

    link: Optional[str] = None
    content: str
    status:bool = True
    seo_title: str
    seo_keywords: str
    seo_description: str
    def get_update_map(self,old_data:dict):
        if self.name != "":
            old_data["name"] = self.name
        if self.description != "":
            old_data["description"] = self.description
        return old_data

class CatecoryData(BaseModel):
    link: Optional[str] = None
    name: str
    content: str

    status:bool = True

    description: str
    seo_title: str
    seo_keywords: str
    seo_description: str
