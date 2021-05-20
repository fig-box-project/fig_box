from app.models.assets import assets
from app.models.character import character
from app.models.editor import editor
from app.models.homepage import homepage
from app.models.jsonsaver import jsonsaver
from app.models.module import moudle
from app.models.settings.crud import settings
from app.models.test import test
from app.models.user import user


def get_module_list():
    rt = [test, homepage, user, assets, character, editor, moudle, jsonsaver]
    read_mods(rt)
    return rt


def read_mods(mods: list):
    mod_strs: list = settings.value['mods']
    for s in mod_strs:
        import_str = f'from app.insmodes.{s} import {s} as mod'
        # try:
        exec(import_str)
        append_str = 'mods.append(mod)'
        exec(append_str)
        # except Exception:
        #     print(f'读[{s}]模组时出错')
