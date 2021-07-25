import datetime
from typing import Union

from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.schedule.mdl_trigger import TriggerMdl


class Trigger:
    def __init__(self, name: str, crontab: str,
                 description: str = '',
                 start_date: datetime.datetime = None,
                 end_date: datetime.datetime = None,
                 is_by_once: bool = False):
        """create a trigger for every [day]
        see https://crontab.guru/ to know how to use
        or you can use [every day 0] to create a trigger to
        fire at 0 every day."""
        if is_by_once:
            if isinstance(start_date, str) and start_date[:6] == 'after ':
                start_date = self.get_date_by_interval(start_date)
            self._trigger = DateTrigger(start_date)
            self._logic = f'd {str(start_date)}'
            self._description = description
            self.name = name
        else:
            if crontab[0:-1] == 'every day ':
                crontab = f'0 {crontab[10:]} * * *'
            self._trigger = CronTrigger.from_crontab(crontab)
            self._logic = f'c {crontab}'
            if start_date is not None:
                self._trigger.start_date = start_date
                self._start_date = start_date
            if end_date is not None:
                self._trigger.end_date = end_date
                self._end_date = end_date
            self._description = description
            self.name = name

    @classmethod
    def by_once(cls, name: str,
                fire_date: Union[datetime.datetime, str] = None,
                description=''):
        """see https://apscheduler.readthedocs.io/en/stable/modules/triggers/date.html?highlight=Trigger
        you can use [after 3d] to fire after 3days,
        you can use [after 4h] to fire after 4 hours,
        you can use [after 50m] to fire after 50 minutes,"""
        return cls(name, '', description, fire_date, is_by_once=True)

    @staticmethod
    def get_date_by_interval(interval: str) -> datetime.datetime:
        params = interval.split(' ')
        if len(params) == 2:
            interval = params[1]
            aim_date = datetime.datetime.now()
            if interval[-1] == 'd':
                days = int(interval[:-1])
                aim_date += datetime.timedelta(days=days)
                return aim_date
            elif interval[-1] == 'h':
                hours = int(interval[:-1])
                aim_date += datetime.timedelta(hours=hours)
                return aim_date
            elif interval[-1] == 'm':
                minutes = int(interval[:-1])
                aim_date += datetime.timedelta(minutes=minutes)
                return aim_date
        raise HTTPException(422, 'type err, check your fire_date')

    @staticmethod
    def get_all_from_database(db: Session):
        return db.query(TriggerMdl).all()

    @staticmethod
    def delete_trigger(db: Session, id: str):
        try:
            id = int(id)
            rt = db.query(TriggerMdl).filter_by(id=id).delete()
            db.commit()
        except ValueError:
            rt = db.query(TriggerMdl).filter_by(name=id).delete()
            db.commit()
        return rt

    def get_trigger(self) -> BaseTrigger:
        """default is every the 0:00 of every day"""
        if self._trigger is None:
            crontab = '0 0 * * *'
            self._trigger = CronTrigger.from_crontab(crontab)
            self._logic = f'c {crontab}'
        return self._trigger

    def get_description(self):
        return self._description

    def get_logic(self) -> str:
        return self._logic

    def insert_to_db(self, db: Session):
        obj = TriggerMdl()
        obj.name = self.name
        obj.description = self.get_description()
        obj.logic = self.get_logic()
        if hasattr(self, '_start_date'):
            obj.start_date = self._start_date
        if hasattr(self, '_end_date'):
            obj.end_date = self._end_date
        obj.create_stamp()
        db.add(obj)
        db.commit()
