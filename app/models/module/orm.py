from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ModuleBase(BaseModel):
    module_name: str

# 自動使用
class ModuleInstall(ModuleBase):
    module_version:int = 1
        
class ModuleUninstall(ModuleBase):
    pass
        
class ModuleUse(ModuleBase):
    pass

class ModuleUnuse(ModuleBase):
    pass
