from typing import Dict

# from app.models.assets import assets
# from app.models.category import category
# from app.models.character import character
# from app.models.editor import editor
# from app.models.homepage import homepage
# from app.models.jsonsaver import jsonsaver
from app.models.log import log
from app.models.module import moudle, AuthModule, TableModule
# from app.models.photo import photo
from app.models.schedule import schedule
from app.models.settings.crud import settings
from app.models.test import test
# from app.models.user import user


def get_module_list() -> dict:
    # create module list
    all_mods = [moudle, schedule, test, log,]
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
        import_str = f'from app.insmodes.{s} import {s} as mod'
        append_str = 'mods.insert(1,mod)'
        # try:
        exec(import_str)
        exec(append_str)
        # except Exception:
        #     print(f'error when read [{s}] module')
