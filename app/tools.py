import requests
from settings import Config

def get_weather(city="Kharkiv") -> int | dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params={
        "q": city,
        "appid": Config.API_KEY,
        "lang": "ua",
        "units": "metric"
    })
    if response.status_code == 200:
        return response.json()
    return response.status_code
