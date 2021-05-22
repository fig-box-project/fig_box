# 防止循环调用,请不要从这里import太多其它模组
from sqlalchemy import func
from sqlalchemy.orm import Query, Session
from starlette.requests import Request

from app.models.settings.crud import settings


class Tools:
    @staticmethod
    def get_assets_url(path: str, request: Request = None):
        """ path: 加前斜杠
        从资源的相对路径来获取url"""
        host = Tools.__get_host(request)
        if Tools.__is_https(request):
            prefix = f'https://{host}/assets{path}'
        else:
            prefix = f'http://{host}/assets{path}'
        return prefix

    @staticmethod
    def __get_host(request: Request):
        host = None
        if request is not None:
            host = request.headers.get('host')
        if host is None:
            host = settings.value['host']
        return host

    @staticmethod
    def __is_https(request: Request):
        is_https = settings.value['is_https']
        if request is not None:
            is_https = request.headers.get('referer') == 'https'
        return is_https

    @staticmethod
    def get_user_ip(request: Request) -> str:
        return request.client.host


class GetListDepend:
    def __init__(self, page_index: int, page_size: int):
        self.page_index = page_index
        self.page_size = page_size
        self.__data = None

    def search(self, query: Query) -> list:
        self.__data = query.offset((self.page_index - 1) * self.page_size) \
            .limit(self.page_size).all()
        return self.__data

    def get_request(self, db: Session, cls, filter_by=None):
        """cls中放HasidMdl的class"""

        if filter_by is None:
            count = db.query(func.count(cls.id)) \
                .scalar()
            data = db.query(cls) \
                .offset((self.page_index - 1) * self.page_size) \
                .limit(self.page_size).all()
        else:
            count = db.query(func.count(cls.id)) \
                .filter(filter_by) \
                .scalar()
            data = db.query(cls) \
                .filter(filter_by) \
                .offset((self.page_index - 1) * self.page_size) \
                .limit(self.page_size).all()
        return {
            'data': data,
            'count': count,
            'page_size': self.page_size,
            'page': self.page_index
        }
