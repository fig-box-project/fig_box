from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter

from app.models.module import ApiModule

ScheduleTool = AsyncIOScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(url='sqlite:///schedule.sqlite')
    }
)
ScheduleTool.start()


def test_job():
    print('ran job')


class Schedule(ApiModule):

    def _register_api_bp(self, bp: APIRouter):
        @bp.get('/all', description='获取所有运行中的任务')
        def get_all():
            return ScheduleTool.get_jobs()

        @bp.get('/start', )
        def start():
            res = ScheduleTool.get_job(job_id='1')
            if res:
                return 'failed'
            job = ScheduleTool \
                .add_job(test_job, 'interval', minutes=1,
                         id='1', replace_existing=True)
            return job.id

    def _get_tag(self) -> str:
        return '预定任务'

    def get_module_name(self) -> str:
        return 'schedule'


schedule = Schedule()
