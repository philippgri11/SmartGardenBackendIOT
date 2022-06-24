import threading

from flask import Flask

from src.controlGPIO import setupGPIO
from src.scheduler import start


def create_app():
    print('create_app')
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    threading.Thread(target=start())
    setupGPIO()
    return app

from src.main import app

if __name__ == "__main__":
    app.run()