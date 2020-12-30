from fastapi import APIRouter, HTTPException, Body, Request, File,UploadFile
from . import crud
from app.main import check_token
from app.models.user.mdl import User
import app.conf as conf

bp = APIRouter()

@bp.get("/photo/{name}")
def photo(name: str):
    return crud.read(name)

@bp.post(conf.url_prefix + '/photo/upload',description = '上传文件')
async def upload(name: str=Body(...),file: UploadFile = File(...)):
    rt = await crud.create_file(file,name)
    if rt == None:
        raise HTTPException(status_code=404,detail='已存在图片')
    elif rt == "over":
        raise HTTPException(status_code=406,detail="图片过大")
    else:
        return rt