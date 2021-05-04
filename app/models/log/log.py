from datetime import date

from loguru import logger


class Log:
    @staticmethod
    def e(message: str = '500'):
        logger.add(f'files/log/500/{date.today()}.log')
        logger.exception(message)
