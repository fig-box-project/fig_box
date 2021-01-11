import os
from starlette.responses import FileResponse
import time
from fastapi import UploadFile

os.makedirs("files", exist_ok=True)
os.makedirs("files/photos", exist_ok=True)

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
    while os.path.exists('files/photos/'+name):
        name_split = name.split(".")
        name_split[-2] += "_"
        name = ".".join(name_split)
    with open('files/photos/'+name, 'wb') as f:
        f.write(res)
    return {'time':time.time() - start,'filename':name,'size':length}