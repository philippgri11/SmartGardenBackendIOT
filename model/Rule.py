import datetime
import json
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

import Database
import controlGPIO


_module_directory = os.path.dirname(os.path.abspath(__file__))
url=os.path.join(_module_directory, 'smartGarden.sqlite')
jobstores = {'default': SQLAlchemyJobStore(url='jdbc:sqlite:C:/Users/Philipp/OneDrive/Dokumente/GitHub/smartGardenBackend/smartGarden.sqlite')}
scheduler = BackgroundScheduler(jobstores=jobstores)


class Rule:
    def __init__(self, *args):
        print(args)
        if len(args) == 5:
            self.id = args[0]
            self.von = args[1]
            self.bis = args[2]
            self.wochentag = args[3]
            self.wetter = args[4]
        elif len(args) == 8:
            self.id = args[0]
            self.von = datetime.time(args[2], args[1])
            self.bis = datetime.time(args[4], args[3])
            self.wochentag = args[5]
            self.wetter = args[6]
        elif isinstance(args[0], tuple):
            zone = args[0]
            self.id = zone[0]
            self.von = datetime.time(zone[2], zone[1])
            self.bis = datetime.time(zone[4], zone[3])
            tag = []
            for char in zone[5]:
                tag.append(True) if (char == '1') else tag.append(False)
            self.wochentag = tag
            self.wetter = zone[6]

    # https: // coderslegacy.com / python / apscheduler - tutorial - advanced - scheduler /

    def turnOn(self):
        controlGPIO.output(Database.getGPIOByRuleID(self.id), 1)
        scheduler.add_job(controlGPIO.output, 'cron', day_of_week=self.getDayOfWeek(), hour=self.von.hour, minute=self.von.minute, id=str(self.id)+'on', args=(Database.getGPIOByRuleID(self.id),1), max_instances = 1, jobstore= 'default')

    def turnOff(self):
        controlGPIO.output(Database.getGPIOByRuleID(self.id), 0)
        scheduler.add_job(controlGPIO.output, 'cron', day_of_week=self.getDayOfWeek(), hour=self.bis.hour, minute=self.bis.minute, id=str(self.id)+'off', args=(Database.getGPIOByRuleID(self.id),0), max_instances = 1, jobstore= 'default')

    def getDayOfWeek(self):
        str = ''
        tage = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        for i in range(len(self.wochentag)):
            if self.wochentag[i]:
                if len(str) > 0:
                    str += ','
                str += tage[i]
        return str


if __name__ == '__main__':
    rule = Rule(Database.getRuleByRuleId(39)[0])
    print(Database.getGPIOByRuleID(39))


class RuleEncoder(json.JSONEncoder):
    def default(self, rule):
        print(rule.id)
        return {'id': rule.id, 'von': {'hours': rule.von.hour, 'minutes': rule.von.minute},
                'bis': {'hours': rule.bis.hour, 'minutes': rule.bis.minute}, 'wochentage': rule.wochentag,
                'wetter': rule.wetter}
