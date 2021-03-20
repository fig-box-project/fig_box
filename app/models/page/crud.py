from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
import os

tempath_prefix = "files/templates"
tem_engine =  Jinja2Templates(tempath_prefix)

class Page:
    def __init__(self,request):
        self.request = request

    def render(self,key:tuple):
        ...

    def show_page(self, template_path: str, data:dict):
        if os.path.exists(f"{tempath_prefix}/{template_path}"):
            data['request'] = self.request
            return tem_engine.TemplateResponse(template_path, data)
        elif os.path.exists(f"{tempath_prefix}/404.html"):
            return tem_engine.TemplateResponse('404.html',{'request':self.request,'err':"模版不存在"})
        else:
            raise HTTPException(404,"找不到404页面")

    def show_404_page(self,err):
        if os.path.exists(f"{tempath_prefix}/404.html"):
            return tem_engine.TemplateResponse('404.html',{'request':self.request,'err':err})
        else:
            raise HTTPException(404,"找不到404页面")

