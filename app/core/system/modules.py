from typing import Dict

# from app.core.assets import assets
# from app.core.category import category
# from app.core.character import character
# from app.core.editor import editor
# from app.core.homepage import homepage
# from app.core.jsonsaver import jsonsaver
from app.core.log import log
# from app.core.photo import photo
from app.core.module_class import AuthModule, TableModule
from app.core.module_manager import module_manager
from app.core.schedule import schedule
from app.core.settings.crud import settings
from app.core.test import test
# from app.core.user import user


def get_module_list() -> dict:
    # create module_manager list
    all_mods = [module_manager, schedule, test, log, ]
    read_mods(all_mods)
    # 分开
    rt: Dict[str, list] = {
        'all': all_mods,
        'auth_mods': [],
        'table_mods': []
    }
    for m in all_mods:
        if isinstance(m, AuthModule):
            rt['auth_mods'].append(m)
        if isinstance(m, TableModule):
            rt['table_mods'].append(m)
    return rt


def read_mods(mods: list):
    """往模组里插入settings文件中引用的模组（不要删未用的arg）"""
    mod_strs: list = settings.value['mods']
    for s in mod_strs:
        import_str = f'from app.modules.{s} import {s} as mod'
        append_str = 'mods.insert(1,mod)'
        # try:
        exec(import_str)
        exec(append_str)
        # except Exception:
        #     print(f'error when read [{s}] module_manager')
