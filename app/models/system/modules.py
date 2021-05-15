from app.models.assets import assets
from app.models.character import character
from app.models.editor import editor
from app.models.homepage import homepage
from app.models.module import moudle
from app.models.test import test
from app.models.user import user


def get_module_list():
    return [test, homepage, user, assets, character, editor, moudle]
