from fastapi.templating import Jinja2Templates
from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session
from app.models.mdl import database
from functools import wraps
import os
import sys

from app.models.template.Template import Template

tempath_prefix = "files/templates"
tem_engine = Jinja2Templates(tempath_prefix)

rending_data = {"now_module": ""}


# 装饰器
def page(func):
    # page(db,request,link)link 当作元组传入
    # func 中将传入(db, link)
    # func 请返回(tamplate, data, [default html]: Html)
    def wrap(params: str, request: Request, db: Session = Depends(database.get_db)):
        params = params.split("/")
        # 判断函数可接受的参数与前端传来的参数数量
        if func.__code__.co_argcount - 1 == len(params):
            rt: tuple = func(db, *params)
            if rt is not None:
                if rt[0] == 404:
                    return Template.response_404(request, rt[1])
                rt[1]['request'] = request
                return Template.response(*rt)
            return Template.response_404(request, '可能在数据库找不到该资源')
        # 返回404
        return Template.response_404(request,
                                     f'路径参数,函数参数不对称: 路径参数: {len(params)}, 函数参数:{func.__code__.co_argcount - 1}')

    return wrap


# 固定的页面
def const_page(func):
    # page(db,request,link)link 当作元组传入
    # func 中将传入(db)
    # func 请返回(tamplate_path, data, [default html]: Html)
    def wrap(request: Request, db: Session = Depends(database.get_db)):
        rt: tuple = func(db)
        if rt[0] == 404:
            return Template.response_404(request,rt[1])
        rt[1]['request'] = request
        return Template.response(*rt)
        # template_path = rt[0]
        # data = rt[1]
        # if os.path.exists(f"{tempath_prefix}/{template_path}"):
        #     data['request'] = request  # request
        #     return tem_engine.TemplateResponse(template_path, data)
        # # 如果404页面存在则返回它
        # if os.path.exists(f"{tempath_prefix}/404.html"):
        #     return tem_engine.TemplateResponse('404.html', {'request': request, 'err': "模版不存在"})
        # else:
        #     raise HTTPException(404, "找不到404页面")

    return wrap


class Page:
    def __init__(self):
        ...

    def wrap(self, is_constant=False):
        """ func 中将传入(db, *link)
        func 请返回(tamplate_path[相对路径(前面不加斜杠)]
        , data, [default html]: Html)
        404页面请返回: 404, message"""
        if is_constant:
            return const_page
        else:
            return page

    def show_page(self, template_path: str, data: dict):
        if os.path.exists(f"{tempath_prefix}/{template_path}"):
            data['request'] = self.request
            return tem_engine.TemplateResponse(template_path, data)
        elif os.path.exists(f"{tempath_prefix}/404.html"):
            return tem_engine.TemplateResponse('404.html', {'request': self.request, 'err': "模版不存在"})
        else:
            raise HTTPException(404, "找不到404页面")
