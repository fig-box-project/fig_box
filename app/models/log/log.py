from fastapi import APIRouter

from app.models.log import UserLogMdl
from app.models.module import ApiModule, TableModule


class Log(ApiModule, TableModule):
    def get_table(self):
        return [UserLogMdl]

    def __init__(self):
        super(Log, self).__init__()

    def _register_api_bp(self, bp: APIRouter):
        """"""
        @bp.get('/user', description='获取用户的logs')
        def get_user_logs():
            """"""


    def _get_tag(self) -> str:
        """"""
        return 'log'

    def get_module_name(self) -> str:
        return 'log'


log = Log()
