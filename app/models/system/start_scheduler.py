from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

scheduler = AsyncIOScheduler()


def run(app: FastAPI):
    @app.on_event('startup')
    def init_scheduler():
        """初始化"""
        jobstores = {
            'default': SQLAlchemyJobStore(url='sqlite:///schedule.sqlite')  # SQLAlchemyJobStore指定存储链接
        }
        executors = {
            'default': {'type': 'threadpool', 'max_workers': 20},  # 最大工作线程数20
            'processpool': ProcessPoolExecutor(max_workers=5)  # 最大工作进程数为5
        }
        global scheduler
        scheduler.configure(jobstores=jobstores, executors=executors)

        print("start scheduler...")

        scheduler.start()
