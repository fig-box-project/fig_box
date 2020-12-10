import jinja2
import os
from sqlalchemy.orm import Session, load_only
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from app.models.article import mdl

templates_path = "files/templates"
templates = Jinja2Templates(directory=templates_path)

# 模版功能
def render_test(request,p:str):
    # test_path = 'index.html'
    if os.path.exists(templates_path +'/'+ p):
        test_data = {'name': '测试名称','request':request}
        return templates.TemplateResponse(p,test_data,)
    else:
        return 'fail'

def render_sitemap():
    return FileResponse('files/sitemap/sitemap.xml',media_type='application/xml')
    # return templates.TemplateResponse(templates_path + '/sitemap.xml',{},media_type='application/xml')

def create_sitemap(db: Session):
    fields = ['link']
    datas = db.query(mdl.Article).options(load_only(*fields)).all()
    lines = []
    first_line = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n'
    lines.append(first_line)
    for i in datas:
        # print(i.link)
        code = \
f'''<url>
<loc>https://www.abc.com/article/{i.link}</loc>
<priority>1.00</priority>
<lastmod>2020-12-09</lastmod>
<changefreq>daily</changefreq>
</url>
'''
        lines.append(code)
    last_line = '</urlset>'
    lines.append(last_line)
    with open('files/sitemap/sitemap.xml','w') as w:
        w.write(''.join(lines))