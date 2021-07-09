from fastapi import APIRouter

from app.models.module import ApiModule
from app.models.schedule.schedule_tool import ScheduleTool
from app.models.tools import Tools
import requests


def test_job():
    trquests.get(http://pi.datasview.com:8081)



class Schedule(ApiModule):
    old_ip = '12.12.12.12'
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
        
        @bp.get('/update', )
        def update():
            return self.check_ip_to_update_domain()
        

    def _get_tag(self) -> str:
        return '预定任务'

    def get_module_name(self) -> str:
        return 'schedule'

    def check_ip_to_update_domain(self):
        """check the ip and when it changed, update to domain sever (
        https://username:password@domains.google.com/nic/update?hostname=subdomain.yourdomain.com&myip=1.2.3.4) """
        
        username = 'ld6wd7WaJbFQpORY'
        password = 'CrCAkky5R62HhqVA'
        full_domain = 'pi.datasview.com'
        now_ip = Tools.get_machine_ip()
        if now_ip != self.old_ip:
            url = f'https://{username}:{password}@domains.google.com/nic/update?hostname={full_domain}&myip={now_ip}'
            response = requests.get(url)
            print('liu-708 reback:' + response.text)
            return response.text
            self.old_ip = now_ip


schedule = Schedule()
