# 防止循环调用,请不要从这里import太多其它模组
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
