# 引用内在的蓝图
from typing import List

from app.core.module_class import Module, PageModule, ApiModule
from app.core.settings.crud import settings
from fastapi import FastAPI, Depends, Request, HTTPException


def check_ip(request: Request):
    # 进入路由时检查IP
    if not settings.value['ip_test_mode']:
        # 如果ip不在允许的列表中时,不允许通过
        if request.client.host not in settings.value['allow_link_ip']:
            raise HTTPException(status_code=400, detail='unallow ip')


def run(app: FastAPI, auto_list: List[Module]):
    # 循环注册
    for m in auto_list:
        if m is not None:
            dependencies = None
            if m.is_need_ip_filter():
                dependencies = [Depends(check_ip)]
            if isinstance(m, PageModule):
                bp_set = m.get_page_bp_set()
                app.include_router(
                    bp_set.get_bp(),
                    prefix=bp_set.get_prefix(),
                    tags=bp_set.get_tags(),
                    dependencies=dependencies
                )
            if isinstance(m, ApiModule):
                bp_set = m.get_api_bp_set()
                app.include_router(
                    bp_set.get_bp(),
                    prefix=bp_set.get_prefix(),
                    tags=bp_set.get_tags(),
                    dependencies=dependencies
                )
