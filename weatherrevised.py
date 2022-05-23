import requests
import math
import time

# intro
print("This program is for finding the best pool temperature to set your heater at to save the most amount of money "
      "whilst still having a good temperature pool.")

city_name = str(input("What City or Town do you live in?\n")).lower()
country_name = str(input("What country do you live in?\n")).upper()
preferred_temp = input("What is your preferred pool temperature?\nCold \nNormal \nWarm \n").lower()
time2 = time.strftime("%X", time.localtime())  # get time
api_key = ""
api_calls = 0

swim_or_not = False

if city_name == "milton":
    city_name = "burlington"


def get_weather(city_name, country_name, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}, {country_name}&appid={api_key}&units=metric"

    response = requests.get(url).json()
    print(response)

    current_temp = response['main']['temp']  # get temp
    print(int(current_temp))

    feels_like = response['main']["feels_like"]  # get feel like
    feels_like = int(feels_like)
    print("This is feels_like " + str(feels_like))

    humidity = response['main']['humidity']
    humidity = int(humidity)
    humidity = str('"' + str(humidity) + '%"')
    print('This is the humidity is ' + str(humidity))

    for item2 in response['weather']:
        current_weather = item2['id']
        if current_weather == '801' or '802' or '800':  # good weather for swimming
            swim_or_not: bool = True

    try:
        warning = response['alerts']
        print(warning)
    except KeyError:
        print("No weather alerts in your local area where found.")


def get_forcast(city_name, country_name, api_key):
    url2 = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name},{country_name}&appid={api_key}&units=metric"
    response2 = requests.get(url2).json()
    for item in response2['list']:
        feels_like_4_hour = round(item['main']['feels_like'])


try:
    get_forcast(city_name, country_name, api_key)
    get_weather(city_name, country_name, api_key)
except TypeError:
    print('TypeError')
