import datetime

from app.models.system.start_scheduler import scheduler


class FigJob:
    def job(self):
        print('job running')

    def start_job(self):
        scheduler.add_job(self.job, 'interval', seconds=5,
                          id='1', replace_existing=True,
                          jobstore="default",
                          executor="default",
                          start_date=datetime.datetime.now(),
                          end_date=datetime.datetime.now() + datetime.timedelta(seconds=240)
                          )
