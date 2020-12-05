import jinja2
import os
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
templates = Jinja2Templates(directory="files/templates")

directory_name = 'files/'
# 存在则是
def check_path_has(path: str):
    return os.path.exists(directory_name + path)
# 模版功能
def render_test(request,p:str):
    # test_path = 'index.html'
    if check_path_has('templates/'+p):
        test_data = {'name': '测试名称','request':request}
        return templates.TemplateResponse(p,test_data)
    else:
        return 'fail'