# 防止循环调用,请不要从这里import太多其它模组
from json import JSONDecodeError

import requests
from fastapi import HTTPException
from requests import Response
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

    @staticmethod
    def get_ip_description(ip: str) -> tuple:
        # rt = {}
        # rt['ip'] = ip
        # 地址获取
        url = 'http://bc.leesinhao.com:3001/api1/v1/ipaddress'
        params = {'ip': ip}
        try:
            response: Response = requests.get(url, params, timeout=(3, 27))
        except requests.exceptions.ConnectionError:
            # 连接错误
            return '服务错误', '服务错误'

        try:
            rq = response.json()
        except JSONDecodeError:
            # json字段错误
            raise HTTPException(500, f'{response.text}不是合法的json')

        try:
            rq = rq['dat']
            if rq['status'] == 0:
                info = rq['result']['ad_info']
                address1 = [
                    info['nation'],
                    info['province'],
                ]
                address2 = [
                    info['city'],
                    info['district']
                ]
                address1 = ','.join(address1)
                address2 = ','.join(address2)
            else:
                address1 = '未知位置'
                address2 = '未知位置'
        except KeyError:
            # 键错误
            return '键问题', '键问题'
        # rt['address1'] = address1
        # rt['address2'] = address2
        return address1, address2


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
        """cls中放HasidMdl的class, 如果传入filter_by将会把它放入filter函数中"""

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


class AuthDepender:
    def __init__(self, auth: int, type: str = 'user_login'):
        ...
