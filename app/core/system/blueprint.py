# 引用内在的蓝图
from typing import List

from app.core.module_class import Module, PageModule, ApiModule, RouteAbleModule
from app.core.module_class.SecurityModule import SecurityModule
from app.core.settings.crud import settings
from fastapi import FastAPI, Depends, Request, HTTPException


def check_ip(request: Request):
    # 进入路由时检查IP
    if not settings.value['ip_test_mode']:
        # 如果ip不在允许的列表中时,不允许通过
        if request.client.host not in settings.value['allow_link_ip']:
            raise HTTPException(status_code=400, detail='unallow ip')


def run(app: FastAPI, auto_list: List[Module]):
    # ループで全部のセキュリティモジュールを獲得する
    security_modules: List[SecurityModule] = []
    for m in auto_list:
        if m is not None:
            if isinstance(m, SecurityModule):
                security_modules.append(m)
    # 循环注册模组
    # ループしてモジュールのルーティングを入れる
    for m in auto_list:
        if m is not None:
            # dependencies = None
            # if m.is_need_ip_filter():
            #     dependencies = [Depends(check_ip)]
            if isinstance(m, PageModule):
                bp_set = m.get_page_bp_set()
                app.include_router(
                    bp_set.get_bp(),
                    prefix=bp_set.get_prefix(),
                    tags=bp_set.get_tags(),
                    # dependencies=dependencies
                )
            if isinstance(m, ApiModule):
                bp_set = m.get_api_bp_set()
                app.include_router(
                    bp_set.get_bp(),
                    prefix="/api/v1" + bp_set.get_prefix(),
                    tags=bp_set.get_tags(),
                    dependencies=get_dependencies(security_modules,m)
                )
            # 自由なプレフィックスを利用するモジュールの為
            if isinstance(m, RouteAbleModule):
                free_prefix_map = m.get_free_prefix_map()
                for k, v in free_prefix_map.items():
                    app.include_router(
                        v.get_bp(),
                        prefix=v.get_prefix(),
                        tags=v.get_tags(),
                        # deprecated=dependencies
                    )


def get_dependencies(security_modules: List[SecurityModule], target: Module):
    dependencies = []
    for i in security_modules:
        depends = i.get_filters(target)
        for j in depends:
            dependencies.append(Depends(j))
    return dependencies
