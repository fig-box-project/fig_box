import datetime

from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.core.mdl import database
from app.core.schedule.FigJob import FigJob
from app.core.schedule.Trigger import Trigger
from app.core.system.start_scheduler import scheduler


def test_job():
    print('running job')


def schedule_route(bp: APIRouter):
    trigger_route(bp)

    @bp.get('/all', description='获取所有运行中的任务')
    def get_all():
        ls = scheduler.get_jobs()
        rt = {}
        for i in ls:
            trigger = i._trigger
            job_type = {}
            if isinstance(trigger, IntervalTrigger):
                job_type['name'] = 'IntervalTrigger'
                job_type['start_date'] = trigger.start_date
                job_type['end_date'] = trigger.end_date
            else:
                job_type['name'] = type(trigger).__name__

            rt[i.id] = {
                'id': i.id,
                'func_name': i.name,
                'state': 'running',
                'type': job_type,
                'next_run_time': i.next_run_time,
                'misfire_grace_time': i.misfire_grace_time,  # how late the job allowed(seconds)
            }
        return rt

    @bp.get('/start', )
    def start():
        # res = ScheduleTool.get_job(job_id='1')
        # if res:
        #     return 'failed'
        # job = scheduler \
        #     .add_job(test_job, 'interval', seconds=5,
        #              id='1', replace_existing=True,
        #              jobstore="default",
        #              executor="default",
        #              start_date=datetime.datetime.now(),
        #              end_date=datetime.datetime.now() + datetime.timedelta(seconds=240)
        #              )
        FigJob().start_job()
        # ScheduleTool.start()
        # asyncio.get_event_loop().run_forever()
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        return "job.id"

    @bp.get('/update', )
    def update():
        """"""
        # return self.check_ip_to_update_domain(False)


def trigger_route(bp: APIRouter):
    @bp.post('/trigger/create/date', description='create a date trigger to trigger list')
    def create_date_trigger(fire_date: datetime.datetime = Body(...),
                            name: str = Body(...),
                            description: str = Body(...),
                            db: Session = Depends(database.get_db)):
        tr = Trigger.by_once(name, fire_date, description)
        tr.insert_to_db(db)
        return {
            'insert': '1'
        }

    @bp.get('/trigger/ls', description='get all of triggers')
    def get_all_triggers(db: Session = Depends(database.get_db)):
        return Trigger.get_all_from_database(db)

    @bp.delete('/trigger/delete', description='delete trigger by id, you can also input a trigger name')
    def delete_trigger(id: str, db: Session = Depends(database.get_db)):
        return {
            'count': Trigger.delete_trigger(db, id)
        }
