from flask import Flask
from src.scheduler import scheduler

def create_app():
    print('hier')
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    scheduler.start()
    return app
