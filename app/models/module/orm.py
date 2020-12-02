from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ModuleBase(BaseModel):
    pass

class ModuleInstall(ModuleBase):
    module_name: str
    module_version:int = 1