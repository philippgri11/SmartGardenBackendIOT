from RestApi import api
from scheduler import scheduler, scheduleTasks

if __name__ == '__main__':
    scheduler.start()
    scheduleTasks()
    api.run()
