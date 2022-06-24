import json

import requests
with open("src/environment.json") as f:
    d = json.load(f)
    api_key = d["api_key"]
    base_url = d["base_url"]
    lat = d["lat"]
    lon = d["lon"]
    exclude = d["exclude"]


complete_url = base_url + "?appid=" + api_key + "&lat=" + lat + "&lon="+ lon + "&exclude=" +exclude

def getRainThisDay():
    response = requests.get(complete_url)
    weatherData = response.json()
    rain = 0
    if 'rain' in weatherData:
        rain = weatherData['daily'][0]['rain']
    return rain

if __name__ == '__main__':
    print(getRainThisDay())