from fastapi import APIRouter, HTTPException, Depends,Header,Body, Request
from . import crud, cache
from app.main import check_token
from app.models.user.mdl import User
from fastapi.templating import Jinja2Templates
from app.models.settings.crud import settings

from sqlalchemy.orm import Session
from app.models import database

templates_path = "files/templates"
templates = Jinja2Templates("files/templates")

bp = APIRouter()

# 获取渲染设置
rander_settings = settings.value["render"]

@bp.get('/api/v1/render/ls', description = '查看有什么在渲染中')
def render_ls():
    rt = []
    for k,v in rander_settings.items():
        children = []
        for kp,vp in v["funs"].items():
            children.append({
                'name':kp, 
                'description': vp["description"], 
                'link_para':vp["link_para"], 
                'query_para':vp["query_para"]
            })
        rt.append({'module': k, 'prefix':v['prefix'], 'count':len(v["funs"]), 'children':children})
    return rt


# 从settings读取数据并设置侦听
# from app.insmodes.article.rander import pull as article_render
# @bp.get('/article/{link}', description='aaa')
# def article_page(link, request: Request, db: Session=Depends(database.get_db)):
#     return article_render.Render().page(db,request,templates,link)


# 从settings的渲染中, 读取每个模组并设置侦听
for k,v in rander_settings.items():
    # 判断是外部模组还是内部模组
    if k[0] == "_":
        k = k[1:]
        exec(f"from app.models.{k} import render as {k}_render")
    else:
        exec(f"from app.insmodes.{k} import render as {k}_render")

    # 循环模组中需侦听的函数
    for kp,vp in v["funs"].items():
        # 获得链接参数
        link_para = vp["link_para"]
        link_url_path = ''.join(['/{' + x + '}' for x in link_para])

        # 获得quary参数
        query_para = vp["query_para"]
        fun_para = ', '.join(link_para + query_para + ["request: Request", "db: Session=Depends(database.get_db)"])
        into_fun_para = ', '.join(['db','request','templates'] + link_para + query_para)
        # 编个执行字符
        route_code = \
f"""@bp.get('{v["prefix"]}{vp["prefix"]}{link_url_path}', description='{vp["description"]}')
def {k}_{kp}({fun_para}):
    return {k}_render.Render().{kp}({into_fun_para})
"""
        exec(route_code) 
