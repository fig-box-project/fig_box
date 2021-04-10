from fastapi import APIRouter, HTTPException

bp = APIRouter()

@bp.get('/packup/directory', description = '打包文件夹')
async def packup():
    from app.models.assets.input_assets_connector.InputZipDirConnector import InputZipDirConnector
    connector = InputZipDirConnector("packup","test.zip","files/templates")
    await connector.packup()