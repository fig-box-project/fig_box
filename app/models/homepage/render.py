import os
from app.models.settings.crud import settings

class Render():
    def __init__(self):
        # 如果模版不存在则创建
        path = 'files/templates/homepage.html'
        if not os.path.exists(path):
            with open(path, 'a') as f:
                f.write("<a href="docs">api</a>")

    def page(self, db, request, templates):
        data = {}
        data['request'] = request
        return templates.TemplateResponse("homepage.html", data)