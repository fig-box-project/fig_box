from fastapi import APIRouter, HTTPException

bp = APIRouter()

@bp.get('/packup/directory', description = '打包文件夹')
async def packup():
    from app.models.assets.input_assets_connector.InputZipDirConnector import InputZipDirConnector
    connector = InputZipDirConnector("packup","test.zip",["settings.yml","files/templates"])
    await connector.packup()

@bp.get('/packup/download', description = "Download")
async def download():
    from app.models.assets.input_assets_connector.InputDownloadConnector import InputDownloadConnector
    connector = InputDownloadConnector("test", "tt312.jpg", "https://lh3.googleusercontent.com/ogw/ADGmqu8m5HjUhjl1CgV_0NyPrbBTAcsgpWMC2p1LSi0=s64-c-mo")
    await connector.packup()