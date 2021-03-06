version = "α228.144"

import jwt
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from app.models import database
from fastapi import FastAPI,Depends,Header,HTTPException,Request
from fastapi.responses import HTMLResponse
from app.models.settings.crud import settings


# 删除settings的模版
mods:dict = settings.value["mods"]

# 引用一下mdl才能创建该数据表
from app.models.user import mdl as user
from app.models.tree import mdl as tree_mdl

# 默认表
tables_strs = ["user.User.__table__","tree_mdl.Category.__table__"]
tables = []

# 自动引用安装的库
for k in mods.keys():
    if "has_mdl" in mods[k]:
        if mods[k]["has_mdl"] == True:
            # 引用下
            exec("from app.insmodes.{0} import mdl as {0}_mdl".format(k))
            # 加入下列表中等下读取
            tables_strs.append("{}_mdl.{}.__table__".format(k,k.capitalize()))

# 录入到tables中
for t in tables_strs:
    exec("tables.append({})".format(t))


# もしテーブルを選びたい時： create_all(bind=engine, tables=[User.__table__])
# もし改めてテーブルを作りたい時： create_all(bind=engine, checkfirst=False)
database.Base.metadata.create_all(bind=database.engine,tables=tables)

# database.Base.metadata.query
# 初始化数据库
db: Session = sessionmaker(bind=database.engine)()
if db.query(user.User).count() == 0:
    print("---create datas---")
    # add admin
    admin_user = user.User(
        username="admin",
        character="master"
    ) 
    admin_user.hash_password("admin")
    db.add(admin_user)
    # add test user
    test_user = user.User(
        username="test",
        character="normal"
    )
    test_user.hash_password("test")
    db.add(test_user)
    
    db.commit()

# app = FastAPI(docs_url=None, redoc_url=None) #关闭文档
# 设置标题,说明,版本
app = FastAPI(
    title = "F-Mod",
    description = "这是自由、易管理的高速模组化cms system.",
    version = version
)

# 进入路由时检测token
# 通过在路由函数中加入这个开启验证并获得用户: now_user:User = Depends(check_token)
def check_token(token: Optional[str] = Header(None)):
    # 在测试模式时总是进入管理员
    if settings.value['auth_test_mode']:
        user_o = db.query(user.User).filter(user.User.id==1).first()
        return user_o
    # 否则检查token合法性
    else:
        user_id = verify_token(token)
        if user_id == None:
            raise HTTPException(status_code=400,detail='token error')
        else:
            return db.query(user.User).filter_by(id=user_id).first()

# 进入路由时检查IP
def check_ip(request: Request):
    if settings.value['ip_test_mode'] == False:
        # 如果ip不在允许的列表中时,不允许通过
        if request.client.host not in settings.value['allow_link_ip']:
            raise HTTPException(status_code=400,detail='unallow ip')

# 验证token
def verify_token(token):
    try:
        data = jwt.decode(token, settings.value['token_key'],algorithms=['HS256'])
    except:
        return None
    return data['id']

# 蓝图
url_prefix = settings.value['url_prefix']
from .models.user.route import bp as user_route
app.include_router(
    user_route,
    prefix=url_prefix + '/auth',
    tags=['用户'],
    dependencies=[Depends(check_ip)])
from .models.assets.route import bp as assets_route
app.include_router(
    assets_route,
    tags=['资源: 图片,打包文件,xml文件等'],
    dependencies=[Depends(check_ip)])
from .models.character.route import bp as chara_route
app.include_router(
    chara_route,
    prefix=url_prefix + '/character',
    tags=['角色'],
    dependencies=[Depends(check_ip)])
    # dependencies=[Depends(check_token)]) 如果想整个包都用户验证而不需要获得用户时用这个
from .models.tree.route import bp as tree_route
app.include_router(
    tree_route,
    prefix=url_prefix + '/category/articles',
    tags=['文章分类'],
    dependencies=[Depends(check_ip)])
from .models.editor.route import bp as editor_route
app.include_router(
    editor_route,
    prefix=url_prefix + '/editor',
    tags=['文件编辑'],
    dependencies=[Depends(check_ip)])
from .models.module.route import bp as module_route
app.include_router(
    module_route,
    prefix=url_prefix + '/moudle',
    tags=['模组・插件'],
    dependencies=[Depends(check_ip)])
from .models.render.route import bp as render_route
app.include_router(
    render_route,
    tags=['页面渲染'],)
from .models.jsaver.route import bp as jsaver_route
app.include_router(
    jsaver_route,
    prefix=url_prefix + '/customfields',
    tags=['json储存'],
    dependencies=[Depends(check_ip)])
from .models.photo.route import bp as photo_route
app.include_router(
    photo_route,
    prefix=url_prefix + '/photo',
    tags=['图片上传,并转为资源'],
    dependencies=[Depends(check_ip)])
from .models.packager.route import bp as packager_route
app.include_router(
    packager_route,
    prefix=url_prefix + '/packager',
    tags=['打包下载的集中管理接口'])

# 用于include入蓝图的文本
include_str = """\
from .insmodes.{0}.route import bp as {0}_route
app.include_router(
    {0}_route,
    prefix=url_prefix + '/{1}',
    tags=[{2}],
    dependencies=[Depends(check_ip)])
"""

# TODO: test
# 自动包括 
for k in mods.keys():
    # 编辑下tags
    tags_li = ['"' + x + '"' for x in mods[k]["route"]["tags"]]
    # 注入模组名,路由前缀,分类标记
    s = include_str.format(k, mods[k]["route"]["route_prefix"], ",".join(tags_li))
    # 引用下
    exec(s)

# @app.get('/',tags=['测试'],response_class=HTMLResponse)
# def root(request: Request):
#     return "<a href=\"docs\">api</a>" + request.client.host + " | " 



