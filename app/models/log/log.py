from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.log import UserLogMdl
from app.models.mdl import database
from app.models.module import ApiModule, TableModule
from app.models.system.check_token import token
from app.models.tools import GetListDepend
from app.models.user import UserMdl


class Log(ApiModule, TableModule):
    def get_table(self):
        return [UserLogMdl]

    def __init__(self):
        super(Log, self).__init__()

    def _register_api_bp(self, bp: APIRouter):
        """"""

        @bp.get('/user', description='获取用户的logs')
        def get_user_logs(db: Session = Depends(database.get_db),
                          now_user: UserMdl = Depends(token.check_token),
                          ls_depend: GetListDepend = Depends()):
            """"""
            condition = UserLogMdl.user_id == now_user.id
            return ls_depend.get_request(db, UserLogMdl, condition)

    def _get_tag(self) -> str:
        """"""
        return 'log'

    def get_module_name(self) -> str:
        return 'log'


log = Log()
