import json
import time

import Database
import controlGPIO
from Database import getAllRules
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
import os

from model.Rule import Rule

with open('environment.json') as f:
    d = json.load(f)
    databaseName = d["databaseName"]

_module_directory = os.path.dirname(os.path.abspath(__file__))
url = os.path.join(_module_directory, databaseName)
jobstores = {'default': SQLAlchemyJobStore(url='sqlite:///' + url)}
scheduler = BackgroundScheduler(jobstores=jobstores)


def scheduleTurnOn(rule):
    print(rule.getDayOfWeek())
    scheduler.add_job(controlGPIO.output, 'cron', day_of_week=rule.getDayOfWeek(), hour=rule.von.hour,
                      minute=rule.von.minute, id=str(rule.id) + 'on', args=(Database.getGPIOByRuleID(rule.id), 1),
                      max_instances=1, jobstore='default')


def scheduleTurnOff(rule):
    scheduler.add_job(controlGPIO.output, 'cron', day_of_week=rule.getDayOfWeek(), hour=rule.bis.hour,
                      minute=rule.bis.minute, id=str(rule.id) + 'off', args=(Database.getGPIOByRuleID(rule.id), 0),
                      max_instances=1, jobstore='default')


def scheduleTasks():
    rules = getAllRules()
    for rule in rules:
        scheduleJob(Rule(rule))


def scheduleJob(rule: Rule):
    if scheduler.get_job(str(rule.id) + 'on') is None:
        scheduleTurnOn(rule)
    else:
        modifyJob(rule, str(rule.id) + 'on')
    if scheduler.get_job(str(rule.id) + 'off') is None:
        scheduleTurnOff(rule)
    else:
        modifyJob(rule, str(rule.id) + 'off')


def modifyJob(rule: Rule, jobID):
    print('modify')
    if jobID.endswith('on'):
        trigger = CronTrigger(day_of_week=rule.getDayOfWeek(), hour=rule.von.hour,
                              minute=rule.von.minute)
        scheduler.get_job(jobID).modify(trigger=trigger)
    if jobID.endswith('off'):
        trigger = CronTrigger(day_of_week=rule.getDayOfWeek(), hour=rule.bis.hour,
                              minute=rule.bis.minute)
        scheduler.get_job(jobID).modify(trigger=trigger)


def removeJob(ruleID):
    if scheduler.get_job(str(ruleID) + 'on') is not None:
        scheduler.remove_job(str(ruleID) + 'on')
    if scheduler.get_job(str(ruleID) + 'off') is not None:
        scheduler.remove_job(str(ruleID) + 'off')


if __name__ == '__main__':
    scheduler.start()
    scheduler.print_jobs()
    print(scheduler.get_jobs(jobstore='default'))
    print(scheduler.get_job(job_id='39on', jobstore='default'))
