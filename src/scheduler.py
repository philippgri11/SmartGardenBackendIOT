import json

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.controlGPIO import output
from src.Rule import Rule

with open("src/environment.json") as f:
    d = json.load(f)
    databaseName = d["databaseName"]
    databasePath = d["databasePath"]


jobstores = {'default': SQLAlchemyJobStore(url='sqlite:///' + databasePath)}
scheduler = BackgroundScheduler(jobstores=jobstores)


def scheduleTurnOn(rule, GPIO):
    print(rule.getDayOfWeek())
    scheduler.add_job(output, 'cron', day_of_week=rule.getDayOfWeek(), hour=rule.von.hour,
                      minute=rule.von.minute, id=str(rule.id) + 'on', args=(GPIO, 1),
                      max_instances=1, jobstore='default')


def scheduleTurnOff(rule, GPIO):
    scheduler.add_job(output, 'cron', day_of_week=rule.getDayOfWeek(), hour=rule.bis.hour,
                      minute=rule.bis.minute, id=str(rule.id) + 'off', args=(GPIO, 0),
                      max_instances=1, jobstore='default')


def createNewJob(rule: Rule, GPIO):
    scheduleTurnOn(rule, GPIO)
    scheduleTurnOff(rule, GPIO)


def modifyJob(rule: Rule):
    jobID = str(rule.id) + 'on'
    trigger = CronTrigger(day_of_week=rule.getDayOfWeek(), hour=rule.von.hour,
                          minute=rule.von.minute)
    scheduler.get_job(jobID).modify(trigger=trigger)
    jobID = str(rule.id) + 'off'
    trigger = CronTrigger(day_of_week=rule.getDayOfWeek(), hour=rule.bis.hour,
                          minute=rule.bis.minute)
    scheduler.get_job(jobID).modify(trigger=trigger)


def removeJob(ruleID):
    if scheduler.get_job(str(ruleID) + 'on'):
        scheduler.remove_job(str(ruleID) + 'on')
    if scheduler.get_job(str(ruleID) + 'off'):
        scheduler.remove_job(str(ruleID) + 'off')


if __name__ == '__main__':
    scheduler.start()
    scheduler.print_jobs()
    print(scheduler.get_jobs(jobstore='default'))
    print(scheduler.get_job(job_id='39on', jobstore='default'))
