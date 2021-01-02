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
    start = time.time()
    res = await file.read()
    length = len(res)
    # 检查后缀
    if name.split(".")[-1] not in ("jpg","jpeg","gif","png","bmp","webp"):
        return "false"
    # 检查大小
    if length > 5000000:
        return "over"
    path = 'files/photos/'+name
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            f.write(res)
        return {'time':time.time() - start,'filename':name,'size':length}
    else:
        return None