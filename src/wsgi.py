import json
import threading

from flask import Flask
import RPi.GPIO as GPIO

from src.scheduler import start
with open("src/environment.json") as f:
    d = json.load(f)
    rainThreshold = d["rainThreshold"]
    channel = d["GPIOchannel"]

def create_app():
    print('create_app')
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    setupGPIO()
    return app

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)