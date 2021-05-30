from fastapi import APIRouter

from app.models.module import ApiModule


class Log(ApiModule):
    def __init__(self):
        super(Log, self).__init__()

    def _register_api_bp(self, bp: APIRouter):
        """"""

    def _get_tag(self) -> str:
        """"""
        return 'log'

    def get_module_name(self) -> str:
        return 'log'


log = Log()
