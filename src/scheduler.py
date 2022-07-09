import json
import rpyc
from src.Rule import Rule

with open("/home/pi/smartGardenBackendIOT/src/environment.json") as f:
    d = json.load(f)
    databaseName = d["databaseName"]
    databasePath = d["databasePath"]
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
conn = rpyc.connect('localhost', 12345, config = rpyc.core.protocol.DEFAULT_CONFIG)

def scheduleGPIO(rule, GPIO, status):
    if status:
        id=str(rule.id) + 'on'
    else:
        id =str(rule.id) + 'off'
    conn.root.addJob(day_of_week=rule.getDayOfWeek(), hour=rule.bis.hour,
                      minute=rule.bis.minute, id=id, status=status, GPIO=GPIO)


def createNewJob(rule: Rule, GPIO):
    scheduleGPIO(rule, GPIO, True)
    scheduleGPIO(rule, GPIO, False)

def modifyJob(rule: Rule):
    jobID = str(rule.id) + 'on'
    print('modifyJob: rule of days')
    print(rule.getDayOfWeek())
    print(rule.wochentag)
    conn.root.modifyJob(job_id= jobID,day_of_week=rule.getDayOfWeek(), hour=rule.von.hour,
                          minute=rule.von.minute)
    jobID = str(rule.id) + 'off'
    conn.root.modifyJob(job_id= jobID, day_of_week=rule.getDayOfWeek(), hour=rule.bis.hour,
                          minute=rule.bis.minute)


def removeJob(ruleID):
    if conn.root.get_job(str(ruleID) + 'on'):
        conn.root.remove_job(str(ruleID) + 'on')
    if conn.root.get_job(str(ruleID) + 'off'):
        conn.root.remove_job(str(ruleID) + 'off')
