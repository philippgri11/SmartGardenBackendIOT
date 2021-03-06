import json
from src.weather import getRainThisDay

with open("src/environment.json") as f:
    d = json.load(f)
    rainThreshold = d["rainThreshold"]

def output(chanel, value):
    if value==1:
        if checkBeforeExcecute():
            print(f"GPIO {chanel}: {value}")
    else:
        print(f"GPIO {chanel}: {value}")

def checkBeforeExcecute():
    return rainThreshold < getRainThisDay()