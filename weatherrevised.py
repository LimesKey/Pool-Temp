import requests
import math
import time

# intro
print("This program is for finding the best pool temperature to set your heater at to save the most amount of money "
      "whilst still having a good temperature pool.")

city_name = str(input("Where are you located?\n")).lower()
city_name = city_name + ",CA"
preferred_temp = input("What is your preferred pool temperature?\nCold \nNormal \nWarm \n").lower()
time2 = time.strftime("%X", time.localtime())  # get time
api_key = "baad0e96d75cca8f793a94da267ab771"
api_calls = 0
api_lock = False
if api_calls > 900:
    api_lock = True

count = 0
run = True

swim_or_not = False

if city_name == "milton,CA":
    city_name = "toronto"
if count + - 1:
    api_calls = 0


def get_weather(api_key, city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

    response = requests.get(url).json()
    print(response)

    current_temp = response['main']['temp']  # get temp
    current_temp = current_temp - 273.15
    print(int(current_temp))

    feels_like = response['main']["feels_like"]  # get feel like
    feels_like = feels_like - 273.15
    feels_like = int(feels_like)
    print("This is feels_like " + str(feels_like))

    humidity = response['main']['humidity']
    humidity = int(humidity)
    humidity = str('"' + str(humidity) + '%"')
    print('This is the humidity is ' + str(humidity))

    current_weather = response['weather']['id']
    if current_weather == '801' or '802' or '800':  # good weather for swimming
        swim_or_not = True

    try:
        warning = response['alerts']
        print(warning)
    except KeyError:
        print("No weather alerts in your local area where found.")



def get_forcast(api_key):
    url2 = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?q={city_name},{'CA'}&appid={api_key}"
    response2 = requests.get(url2).json()
    print(response2)
    for item in response2['list']:
        response2 = requests.get(url2).json()
        print(response2)
        feels_like_4_hour = response2['main']['feels_like']


get_forcast(api_key)

try:
    get_weather(api_key, city_name)
except traceback:
    print()