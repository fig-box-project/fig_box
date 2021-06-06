from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.models.assets.input_assets_connector import *
from fastapi import APIRouter, HTTPException, Depends

from app.models.category import mdl
from app.models.log.log_tools import LogTools
from app.models.mdl import database
from app.models.mdl import PageMdl
from app.models.settings.crud import settings
from app.models.tools import Tools


def test_route(bp: APIRouter):
    # @bp.get('/packup/directory', description='打包文件夹')
    # async def packup():
    #     connector = InputZipDirConnector(
    #         "packup", "test.zip", ["settings.yml", "files/templates"], False)
    #     # connector.set_zip_mode(InputZipDirConnector.WRAP_IN_ROOT)
    #     # connector.set_zip_mode(InputZipDirConnector.WRAP_WITH_INDEX)
    #     connector.set_zip_mode(InputZipDirConnector.WRAP_WITH_PATH)
    #     await connector.packup()
    #
    #     # connector = OutputUnzipConnector('packup/test.zip')
    #     # connector.output()
    #
    # @bp.get('/packup/download', description="Download")
    # async def download():
    #     from app.models.assets.input_assets_connector.InputDownloadConnector import InputDownloadConnector
    #     connector = InputDownloadConnector(
    #         "test", "tt312.jpg",
    #         "https://lh3.googleusercontent.com/ogw/ADGmqu8m5HjUhjl1CgV_0NyPrbBTAcsgpWMC2p1LSi0=s64-c-mo")
    #     await connector.packup()
    #
    # @bp.get('/unzip/{l}')
    # def unzip(l: int):
    #     return 5 / 0
    #     # secrets.compare_digest()
    #
    # @bp.get('/test')
    # def test():
    #     print(type(PageMdl))
    #     print(type(DeclarativeMeta))
    #     print(isinstance(PageMdl, DeclarativeMeta))
    #     print(PageMdl.__mro__)
    #     print(PageMdl in PageMdl.__mro__)
    #
    # @bp.get('/category')
    # def category(id: int, db: Session = Depends(database.get_db)):
    #     c: mdl.Category = db.query(mdl.Category).filter_by(id=id).first()
    #
    #     return c.father
    #
    @bp.get('/rere')
    def rere(request: Request):
        return request.headers

    #
    # @bp.get('/settings')
    # def setting():
    #     settings.value['a'] = 'b'
    #
    @bp.get('/log')
    def log():
        LogTools.test()

    # @bp.get('/ip')
    # def ip(request:Request):
    #     return Tools.get_ip_description(request)
