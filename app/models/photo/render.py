import os
from app.models.settings.crud import settings
from starlette.responses import FileResponse
from shutil import copyfile

class Render():
    def __init__(self):
        # 如果模版不存在则创建
        path = 'files/templates/homepage.html'
        if not os.path.exists(path):
            open(path, 'a').close()
        
        # 如果404image不存在则复制过来
        path = 'files/photos/404.jpg'
        if not os.path.exists(path):
            copyfile("404_image.jpg", "files/photos/404.jpg")


    def page(self, db, request, templates, img_name):
        path = 'files/photos/' + img_name
        # 首先查看存在与否
        if os.path.exists(path):
            return FileResponse(path, media_type='image/jpeg')
        else:
            return FileResponse('files/photos/404.jpg', media_type='image/jpeg')