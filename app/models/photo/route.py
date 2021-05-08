from app.models.assets.crud import Assets
from fastapi import APIRouter, HTTPException, Body, Request, File, UploadFile, Depends

from app.models.system.check_token import token
from app.models.user.mdl import User

bp = APIRouter()


@bp.post('/upload', description='上传文件')
async def upload(name: str = Body(...), now_user: User = Depends(token.check_token), photo: UploadFile = File(...)):
    rt = await Assets.upload_with_user(photo, name, now_user, prefix="photos/", limit=5)
    return rt
