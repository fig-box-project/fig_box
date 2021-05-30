from app.models.assets import assets
from app.models.category import category
from app.models.character import character
from app.models.editor import editor
from app.models.homepage import homepage
from app.models.jsonsaver import jsonsaver
from app.models.module import moudle, AuthModule
from app.models.photo import photo
from app.models.settings.crud import settings
from app.models.test import test
from app.models.user import user


def get_module_list() -> dict:
    # create module list
    all_mods = [test, homepage, user, assets, photo, category, character, editor, moudle, jsonsaver]
    read_mods(all_mods)
    # 分开
    rt = {
        'all': all_mods,
    }
    auth_mods = []
    for m in all_mods:
        if isinstance(m, AuthModule):
            auth_mods.append(m)
    rt['auth_mods'] = auth_mods
    return rt


def read_mods(mods: list):
    mod_strs: list = settings.value['mods']
    for s in mod_strs:
        import_str = f'from app.insmodes.{s} import {s} as mod'
        append_str = 'mods.append(mod)'
        try:
            exec(import_str)
            exec(append_str)
        except Exception:
            print(f'读[{s}]模组时出错')
