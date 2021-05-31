from datetime import date

from loguru import logger
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.models.tools import Tools


class LogTools:
    PREFIX = 'files/log'

    @staticmethod
    def e(message: str = '500'):
        logger.remove()
        logger.add(f'{LogTools.PREFIX}/500/{date.today()}.log')
        logger.exception(message)
        logger.info('----------------')

    @staticmethod
    def user_log(status: str, user_id: int,
                 ip:str, address1: str, address2: str):
        """status 0 注册, 1 登录, 其它数字 其它意思"""
        # log到文件
        logger.remove()
        logger.add(f'{LogTools.PREFIX}/user/all.log', rotation='100 MB')
        logger.opt(lazy=True).info(f'ip: {ip}'
                                   f' status:{status} id: {user_id}')

    TIMES = 0

    @staticmethod
    def get_user_logs(user_id: int):
        with open(f'{LogTools.PREFIX}/user/byid/{user_id}.log', 'r') as f:
            return f.read()

    @staticmethod
    def test():
        logger.remove()
        logger.add(f'{LogTools.PREFIX}/test/test.log', rotation='1000 B')
        logger.add(f'{LogTools.PREFIX}/test/test2.log', rotation='1000 B')
        LogTools.TIMES += 1
        logger.info("infohsdafkjhsfls" + str(LogTools.TIMES))
