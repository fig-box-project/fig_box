import asyncio
import datetime

from fastapi import APIRouter

from app.models.module import ApiModule
from app.models.system.start_scheduler import scheduler
from app.models.tools import Tools
import requests


def test_job():
    # requests.get('http://0.0.0.0:8081')
    print('running job')


class Schedule(ApiModule):
    old_ip = '12.12.12.12'

    def _register_api_bp(self, bp: APIRouter):
        @bp.get('/all', description='获取所有运行中的任务')
        def get_all():
            ls = scheduler.get_jobs()
            rt = {}
            for i in ls :
                rt[i.id] = i.name
            return rt

        @bp.get('/start', )
        def start():
            # res = ScheduleTool.get_job(job_id='1')
            # if res:
            #     return 'failed'
            job = scheduler \
                .add_job(test_job, 'interval', seconds=5,
                         id='1', replace_existing=True,
                         jobstore="default",
                         executor="default",
                         start_date=datetime.datetime.now(),
                         end_date=datetime.datetime.now() + datetime.timedelta(seconds=240)
                         )
            # ScheduleTool.start()
            # asyncio.get_event_loop().run_forever()
            # loop = asyncio.new_event_loop()
            # asyncio.set_event_loop(loop)
            return job.id

        @bp.get('/update', )
        def update():
            return self.check_ip_to_update_domain(False)

    def _get_tag(self) -> str:
        return '预定任务'

    def get_module_name(self) -> str:
        return 'schedule'

    def check_ip_to_update_domain(self, is_use_default: bool = True):
        """check the ip and when it changed, update to domain sever (
        https://username:password@domains.google.com/nic/update?hostname=subdomain.yourdomain.com&myip=1.2.3.4) """

        username = 'ld6wd7WaJbFQpORY'
        password = 'CrCAkky5R62HhqVA'
        full_domain = 'pi.datasview.com'
        now_ip = Tools.get_machine_ip()
        if now_ip != self.old_ip:
            url = f'https://{username}:{password}@domains.google.com/nic/update?hostname={full_domain}'
            if not is_use_default:
                url += f'&myip={now_ip}'
            print('liu-714 send:' + url)
            response = requests.get(url)
            # print('liu-708 reback:' + response.text)
            self.old_ip = now_ip
            return response.text


schedule = Schedule()
