import json
from datetime import datetime, timedelta

from src.database import updateStatus
from src.scheduler import scheduler

with open("src/environment.json") as f:
    d = json.load(f)
    timeToWaitRuhemodus = d["timeToWaitRuhemodus"]

def ruhemodusON():
    scheduler.add_job(updateStatus, 'date', run_date=datetime.now()+ timedelta(hours=timeToWaitRuhemodus), args=[False],
                      id='ruhemodusON', max_instances=1, jobstore='default')
    updateStatus(True)

def ruhemodusOFF():
    scheduler.remove_job(job_id='ruhemodusON')
    updateStatus(False)

def setRuhemodus(status):
    if status:
        ruhemodusON()
    else:
        ruhemodusOFF()