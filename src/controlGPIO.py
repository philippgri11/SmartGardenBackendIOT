import json
from src.weather import getRainThisDay
import RPi.GPIO as GPIO
with open("src/environment.json") as f:
    d = json.load(f)
    rainThreshold = d["rainThreshold"]
    channel = d["GPIOchannel"]

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT, initial=GPIO.LOW)

def output(chanel, state):
    if state==1:
        if checkBeforeExcecute():
            print(f"GPIO {chanel}: {state}")
            GPIO.output(channel, state)
    else:
        print(f"GPIO {chanel}: {state}")
        GPIO.output(channel, state)


def checkBeforeExcecute():
    return rainThreshold < getRainThisDay()