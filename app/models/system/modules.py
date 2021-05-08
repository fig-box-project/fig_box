from app.models.homepage import homepage
from app.models.test import test
from app.models.user import user


def get_module_list():
    return [test, homepage, user]
