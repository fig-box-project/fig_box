from datetime import date

from loguru import logger


class Log:
    PREFIX = 'files/log'

    @staticmethod
    def e(message: str = '500'):
        logger.remove()
        logger.add(f'{Log.PREFIX}/500/{date.today()}.log')
        logger.exception(message)
        logger.info('----------------')

    @staticmethod
    def user_log(status: int, user_id: int):
        """status 0 注册, 1 登录, 其它数字 其它意思"""
        logger.remove()
        logger.add(f'{Log.PREFIX}/user/all.log', rotation='100 MB')
        logger.add(f'{Log.PREFIX}/user/byid/{user_id}.log', rotation='5 MB')
        if status == 0:
            status_str = ' register'
        elif status == 1:
            status_str = ' login'
        else:
            status_str = ' other'
        logger.opt(lazy=True).info(f'status:{status_str} id: {user_id}')

    TIMES = 0

    @staticmethod
    def test():
        logger.remove()
        logger.add(f'{Log.PREFIX}/test/test.log', rotation='1000 B')
        Log.TIMES += 1
        logger.info("infohsdafkjhsfls" + str(Log.TIMES))
