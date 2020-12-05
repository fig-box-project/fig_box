from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ModuleBase(BaseModel):
    pass

class Module(ModuleBase):
    name: str = 'comment'
    version: str = '~'

class ModuleStatus(ModuleBase):
    name: str
    version: str
    status: bool
