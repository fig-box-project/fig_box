# 引用内在的蓝图
from app.models.user.route import bp as user_route
from app.models.assets.route import bp as assets_route
from app.models.character.route import bp as chara_route
from app.models.editor.route import bp as editor_route
from app.models.module.route import bp as module_route
# from app.models.render.route    import bp as render_route
from app.models.test.route import bp as test_route
from app.models.jsaver.route import bp as jsaver_route
from app.models.photo.route import bp as photo_route
from app.models.packager.route import bp as packager_route
from app.models.category.route import bp as category_route

from app.models.settings.crud import settings
from fastapi import FastAPI, Depends, Request, HTTPException


def check_ip(request: Request):
    # 进入路由时检查IP
    if settings.value['ip_test_mode'] == False:
        # 如果ip不在允许的列表中时,不允许通过
        if request.client.host not in settings.value['allow_link_ip']:
            raise HTTPException(status_code=400, detail='unallow ip')


def run(app: FastAPI):
    # 蓝图
    url_prefix = settings.value['url_prefix']

    if settings.value['route_test_mode']:
        app.include_router(
            test_route,
            prefix="/test",
            tags=['测试'],
            dependencies=[Depends(check_ip)]
        )

    app.include_router(
        user_route,
        prefix=url_prefix + '/auth',
        tags=['用户'],
        dependencies=[Depends(check_ip)])
    app.include_router(
        assets_route,
        tags=['资源: 图片,打包文件,xml文件等'],
        dependencies=[Depends(check_ip)])

    app.include_router(
        chara_route,
        prefix=url_prefix + '/character',
        tags=['角色'],
        dependencies=[Depends(check_ip)])
    # dependencies=[Depends(check_token)]) 如果想整个包都用户验证而不需要获得用户时用这个
    # from .models.tree.route import bp as tree_route
    app.include_router(
        category_route,
        prefix=url_prefix + '/category',
        tags=['文章的分类'],
        dependencies=[Depends(check_ip)])

    app.include_router(
        editor_route,
        prefix=url_prefix + '/editor',
        tags=['文件编辑'],
        dependencies=[Depends(check_ip)])
    app.include_router(
        module_route,
        prefix=url_prefix + '/moudle',
        tags=['模组・插件'],
        dependencies=[Depends(check_ip)])

    # app.include_router(
    #     render_route,
    #     tags=['页面渲染'],)
    app.include_router(
        jsaver_route,
        prefix=url_prefix + '/customfields',
        tags=['json储存'],
        dependencies=[Depends(check_ip)])

    app.include_router(
        photo_route,
        prefix=url_prefix + '/photo',
        tags=['图片上传,并转为资源'],
        dependencies=[Depends(check_ip)])

    app.include_router(
        packager_route,
        prefix=url_prefix + '/packager',
        tags=['打包下载的集中管理接口'])

    # 页面导入
    from app.models.homepage.page import bp as homepage_page
    app.include_router(
        homepage_page,
        prefix="",
        tags=['首页页面']
    )
