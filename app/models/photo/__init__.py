from fastapi import APIRouter, Body, Depends, UploadFile, File

from app.models.assets.crud import Assets
from app.models.module import ApiModule
from app.models.system.check_token import token
from app.models.user.orm import User


class Photo(ApiModule):
    def _register_api_bp(self, bp: APIRouter):
        @bp.post('/upload', description='上传文件')
        async def upload(name: str = Body(...), now_user: User = Depends(token.check_token),
                         photo: UploadFile = File(...)):
            rt = await Assets.upload_with_user(photo, name, now_user, prefix="photos/", limit=5)
            return rt

    def _get_tag(self) -> str:
        return '图片上传'

    def get_module_name(self) -> str:
        return 'photo'
