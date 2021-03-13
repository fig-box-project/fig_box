from fastapi import APIRouter, HTTPException, Body, Request, File,UploadFile, Depends
from . import crud, orm
from app.main import check_token
from app.models.user.mdl import User

bp = APIRouter()

@bp.post('/upload',description = '上传文件')
async def upload(name: str = Body(...),now_user:User = Depends(check_token), file: UploadFile = File(...)):
    rt = await crud.create_file(file,name)
    if rt == None:
        raise HTTPException(status_code=404,detail='已存在图片')
    elif rt == "over":
        raise HTTPException(status_code=406,detail="图片过大")
    elif rt == "false":
        raise HTTPException(status_code=406,detail="格式不正确")
    else:
        return rt