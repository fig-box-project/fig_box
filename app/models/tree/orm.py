
from typing import List, Optional
from pydantic import BaseModel

class TreeBase(BaseModel):
    pass

class TreeCU(TreeBase):
    id: int
    name: str
