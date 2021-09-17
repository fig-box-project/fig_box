import datetime

from app.core.system.start_scheduler import scheduler


class FigJob:
    def __init__(self):
        self._job = None

    def job(self):
        print('job running')

    def start_job(self):
        self._job = scheduler \
            .add_job(self.job, 'interval', seconds=5,
                     id='1', replace_existing=True,
                     jobstore="default",
                     executor="default",
                     start_date=datetime.datetime.now(),
                     end_date=datetime.datetime.now()
                              + datetime.timedelta(seconds=240)
                     )
