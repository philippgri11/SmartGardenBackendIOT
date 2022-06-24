import json

from src.database import getStatusRuhemodus
from src.weather import getRainThisDay
import RPi.GPIO as GPIO
with open("src/environment.json") as f:
    d = json.load(f)
    rainThreshold = d["rainThreshold"]


def output(channel, state):
    print('output')
    print(checkBeforeExcecute())
    print(rainThreshold)
    print(getRainThisDay())
    print(getStatusRuhemodus())
    if state==1:
        print(f"GPIO {channel}: {state}")
        GPIO.output(channel, GPIO.LOW)
    else:
        print(f"GPIO {channel}: {state}")
        GPIO.output(channel, GPIO.HIGH)

def checkBeforeExcecute():
    return (rainThreshold > getRainThisDay()) and not(getStatusRuhemodus())