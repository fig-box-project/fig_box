from app.models.settings.crud import settings
from fastapi import Depends, Request, HTTPException

# 用于include入蓝图的文本
include_str = """\
from app.insmodes.{0}.route import bp as {0}_route
app.include_router(
    {0}_route,
    prefix=url_prefix + '/{1}',
    tags=[{2}],
    dependencies=[Depends(check_ip)])
"""

mods:dict = settings.value["mods"]

# 进入路由时检查IP
def check_ip(request: Request):
    if settings.value['ip_test_mode'] == False:
        # 如果ip不在允许的列表中时,不允许通过
        if request.client.host not in settings.value['allow_link_ip']:
            raise HTTPException(status_code=400,detail='unallow ip')


def run(app):
    # 不要删除
    url_prefix = settings.value['url_prefix']
    print("---start import mod---\n")
    # 自动包括 
    for k in mods.keys():
        # 编辑下tags
        tags_li = ['"' + x + '"' for x in mods[k]["route"]["tags"]]
        # 注入模组名,路由前缀,分类标记
        s = include_str.format(k, mods[k]["route"]["route_prefix"], ",".join(tags_li))
        print(s)
        # 引用下
        exec(s)
    print("---end import mod---\n")