import asyncio
import datetime

from fastapi import APIRouter

from app.models.module import ApiModule, TableModule
from app.models.schedule.mdl_trigger import TriggerMdl
from app.models.schedule.route import schedule_route
from app.models.system.start_scheduler import scheduler
from app.models.tools import Tools
import requests


def test_job():
    # requests.get('http://0.0.0.0:8081')
    print('running job')


class Schedule(ApiModule, TableModule):
    def get_table(self) -> list:
        return [TriggerMdl]

    old_ip = '12.12.12.12'

    def _register_api_bp(self, bp: APIRouter):
        schedule_route(bp)

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
