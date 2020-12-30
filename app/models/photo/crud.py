import os
from starlette.responses import FileResponse
import time
from fastapi import UploadFile

os.makedirs("files", exist_ok=True)
os.makedirs("files/photos", exist_ok=True)

def read(name: str):
    return FileResponse('files/photos/'+name,media_type='image/jpeg')

# 上传图片
async def create_file(file:UploadFile,name:str):
    if not os.path.exists('files/photos/'+name):
        start = time.time()
        path = 'files/photos/'+name
        res = await file.read()
        with open(path, 'wb') as f:
            f.write(res)
        return {'time':time.time() - start,'filename':name}
    else:
        return None