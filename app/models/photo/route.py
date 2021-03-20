from app.models.assets.crud import Assets
from fastapi import APIRouter, HTTPException, Body, Request, File,UploadFile, Depends
from app.main import check_token
from app.models.user.mdl import User

bp = APIRouter()

@bp.post('/upload',description = '上传文件')
async def upload(name: str = Body(...),now_user:User = Depends(check_token), photo: UploadFile = File(...)):
   rt = Assets.insert_with_user(photo, name, now_user, limit = 5)
   return rt
   