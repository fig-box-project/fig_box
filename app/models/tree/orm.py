
from typing import List, Optional
from pydantic import BaseModel

class CategoryBase(BaseModel):
    pass

class CategoryCU(CategoryBase):
    id: int
    name: str
