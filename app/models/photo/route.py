from fastapi import APIRouter, HTTPException, Body, Request, File,UploadFile
from . import crud
from app.main import check_token
from app.models.user.mdl import User
bp = APIRouter()

@bp.get("/photo/{name}")
def photo(name: str):
    return crud.read(name)

@bp.post('/upload/photo',description = '上传文件')
async def upload(name: str=Body(...),file: UploadFile = File(...)):
    rt = await crud.create_file(file,name)
    if rt == None:
        raise HTTPException(status_code=404,detail='已存在图片')
    else:
        return rt