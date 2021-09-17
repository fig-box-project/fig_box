from typing import List

from app.core.module_manager import AuthModule


def run(ls: List[AuthModule]):
    """为需要权限的模组安置唯一的权限号"""
    auth_key = 2
    for i in ls:
        auth_items = i.get_auth_items()
        for j in auth_items:
            j.set_auth_key(auth_key)
            auth_key += 1
    # call back after all
    for i in ls:
        i.auth_register_callback()
