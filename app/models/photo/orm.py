from typing import List, Optional
from pydantic import BaseModel

class PhotoUpload(BaseModel):
    name: str
    class Config:
        orm_mode= True