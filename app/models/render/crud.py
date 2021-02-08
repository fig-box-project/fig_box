import jinja2
import os
from sqlalchemy.orm import Session, load_only
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from . import conf

# from app.models.article import mdl

# 创建需要的文件夹
os.makedirs("files", exist_ok=True)
os.makedirs("files/templates", exist_ok=True)
os.makedirs("files/templates/article", exist_ok=True)
os.makedirs("files/sitemap", exist_ok=True)
os.makedirs("files/photos", exist_ok=True)

# 不存在则创建默认的404文件
if not os.path.exists("files/templates/404.html"):
    with open("files/templates/404.html", 'w') as f:
        f.write("404 {% if err %}{{ err }}{% endif %}")

templates_path = "files/templates"
templates = Jinja2Templates(directory=templates_path)

# 读取照片
def read(name: str):
    return FileResponse('files/photos/'+name,media_type='image/jpeg')

# 模版功能
def render_test(request,p:str):
    # test_path = 'index.html'
    if os.path.exists(templates_path +'/'+ p):
        test_data = {'name': '测试名称','request':request}
        return templates.TemplateResponse(p,test_data,)
    else:
        return 'fail'

# 渲染文章
# def view_article(link:str,db: Session,request):
#     try:
#         article = db.query(mdl.Article).filter(mdl.Article.link == link).first()
#         if article != None and os.path.exists("files/templates/article/show.html"):
#             data = {}
#             data['pageData'] = article.__dict__
#             data['prevData'] = article.__dict__
#             data['nextData'] = article.__dict__
#             data['request'] = request
#             print("正常")
#             return templates.TemplateResponse("article/show.html", data)
#         else:
#             print("检测出404" + str(article != None) + str(os.path.exists("files/templates/article/show.html")))
#             return templates.TemplateResponse('404.html',{'request':request,'err':"no error"})
#     except Exception as e:
#         print("错误404")
#         return templates.TemplateResponse('404.html',{'request':request,'err':str(e)})

# 渲染列表
def view_list(db: Session,request,begin_id:int,length:int):
    try:
        # 代码
        data = {
            "status": 1,
            "create_date": "2021-01-04T18:56:33.125188",
            "title": "string",
            "link": "1",
            "owner_id": 2,
            "seo_keywords": "string",
            "description": "string",
            "category_id": 0,
            "update_date": "2021-01-04T18:56:33.125217",
            "id": 1,
            "seo_description": "string",
            "seo_title": "string",
            "image": "string",
            "category_name": "root"
        }
        rt = {}
        rt['request'] = request
        rt['listData'] = [data,data,data,data,data,data]
        return templates.TemplateResponse("article/list.html", rt)
    except Exception as e:
        return templates.TemplateResponse('404.html',{'request':request,'err':str(e)})

def render_sitemap():
    return FileResponse('files/sitemap/sitemap.xml',media_type='application/xml')
    # return templates.TemplateResponse(templates_path + '/sitemap.xml',{},media_type='application/xml')
