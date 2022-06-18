from flask import Flask

from src.controlGPIO import setupGPIO
from src.scheduler import scheduler


def create_app():
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    scheduler.start()
    setupGPIO()
    return app

from src.main import app

if __name__ == "__main__":
    app.run()