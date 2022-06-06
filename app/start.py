from flask import Flask
from scheduler import scheduler, scheduleTasks
#
# scheduler.start()
# scheduleTasks()

def create_app():
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # scheduler.start()
    # scheduleTasks()
    return app

