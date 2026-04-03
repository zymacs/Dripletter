from cronconverter import CronConverter
from crontab import CronTab




class CronScheduler:

    def __init__(self, user):
        self.cron = CronTab(user)
        self.cronconverter = CronConverter()
        self.jobs = []
        
    def create_job(self, command):
        job = self.cron.new(command=command)
        self.jobs.append(job)

    def enable_all(self):
        for job in self.jobs:
            job.enable()

    def set_schedule(self, cron_string, from_natural_lang=True):
        if from_natural_lang:
            cron_string = self.cronconverter.parse_sentence(cron_string)
        for job in self.jobs:
            job.setall(cron_string)
            
    def write_all(self):
        self.cron.write()


    def annotate_all(self, comment):
        for job in self.jobs:
            job.set_comment(comment)
    

