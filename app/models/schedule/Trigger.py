from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger


class Trigger:
    def __init__(self):
        self._description = 'At 00:00.'
        self._trigger = None

    def get_trigger(self) -> BaseTrigger:
        if self._trigger is None:
            self._trigger = CronTrigger.from_crontab('0 0 * * *')
        return self._trigger

    def get_description(self):
        return self._description

    def every(self, corntab: str, description: str):
        """create a trigger for every [day]
        see https://crontab.guru/ to know how to use
        or you can use [every day 0] to create a trigger to
        fire at 0 every day."""
        if corntab[0:-1] == 'every day ':
            corntab = f'0 {corntab[10:]} * * *'
        self._trigger = CronTrigger.from_crontab(corntab)
        self._description = description
