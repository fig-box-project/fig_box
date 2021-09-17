from fastapi import APIRouter

from app.core.module_class import ApiModule
from app.core.module_manager.route import module_route


# 下面是api的实现
class ModuleManager(ApiModule):
    def _register_api_bp(self, bp: APIRouter):
        module_route(bp)

    def _get_tag(self) -> str:
        return 'モジュール管理'

    def get_module_name(self) -> str:
        return 'moudle'


module_manager = ModuleManager()
