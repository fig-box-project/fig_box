import os
from app.models.settings.crud import settings
from app.models.page.crud import Page

class Render():
    def __init__(self):
        # 如果模版不存在则创建
        path = 'files/templates/homepage.html'
        if not os.path.exists(path):
            with open(path, 'a') as f:
                f.write('<a href="docs">api</a>')

    def page(self, db, request):
        pg = Page(request)
        data = {}
        return pg.show_page("homepage.html", data)