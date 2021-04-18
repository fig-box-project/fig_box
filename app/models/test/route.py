from app.models.assets.output_assets_connector import OutputUnzipConnector
from fastapi import APIRouter, HTTPException

bp = APIRouter()


@bp.get('/packup/directory', description='打包文件夹')
async def packup():
    from app.models.assets.input_assets_connector.InputZipDirConnector import InputZipDirConnector
    connector = InputZipDirConnector(
        "packup", "test.zip", ["settings.yml", "files/templates"])
    # connector.set_zip_mode(InputZipDirConnector.WRAP_IN_ROOT)
    # connector.set_zip_mode(InputZipDirConnector.WRAP_WITH_INDEX)
    connector.set_zip_mode(InputZipDirConnector.WRAP_WITH_PATH)
    await connector.packup()

    connector = OutputUnzipConnector('packup/test.zip')
    connector.output()


@bp.get('/packup/download', description="Download")
async def download():
    from app.models.assets.input_assets_connector.InputDownloadConnector import InputDownloadConnector
    connector = InputDownloadConnector(
        "test", "tt312.jpg", "https://lh3.googleusercontent.com/ogw/ADGmqu8m5HjUhjl1CgV_0NyPrbBTAcsgpWMC2p1LSi0=s64-c-mo")
    await connector.packup()


@bp.get('unzip')
def unzip():
    connector = OutputUnzipConnector('packup/test.zip')
    connector.output()
