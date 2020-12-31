from typing import List, Optional
from pydantic import BaseModel

class JsaverWrite(BaseModel):
    name: str
    json_str: str
    class Config:
        orm_mode= True