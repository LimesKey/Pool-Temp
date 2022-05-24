import requests
import math
import time

# intro
print("This program is for finding the best pool temperature to set your heater at to save the most amount of money "
      "whilst still having a good temperature pool.")

city_name = str(input("What City or Town do you live in?\n")).lower()
country_name = str(input("What country do you live in?\n")).upper()
preferred_temp = ""
pool_temp_normal = 80
pool_temp_warm = 84  # starting values for pool calcuator temp
pool_temp_cold = 78
# if country_name.upper() == 'CANADA':
# country_name = 'CA'
# if country_name.upper() == 'AMERICA' or 'UNITED STATES' or 'UNITED STATES OF AMERICA' or 'UNITED STATE':
# country_name = 'US'
while preferred_temp != 'normal' or 'cold' != preferred_temp or 'warm' != preferred_temp:
    preferred_temp = input("What is your preferred pool temperature?\nCold, \nNormal, \nWarm, \n").lower()
    if preferred_temp == 'normal' or 'cold' == preferred_temp or 'warm' == preferred_temp:
        break
    else:
        print("You have not selected the correct value")

time2 = time.strftime("%X", time.localtime())  # get time
api_key = ""
api_calls = 0

swim_or_not = False

if city_name == "milton":
    city_name = "Oakville"


def get_weather(city_name, country_name, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}, {country_name}&appid={api_key}&units=metric"

    response = requests.get(url).json()

    current_temp = round(response['main']['temp'])  # get temp
    print(f'The current temp is {current_temp}.')

    feels_like = response['main']["feels_like"]  # get feel like
    feels_like = int(feels_like)
    print(f"This is feels like {feels_like}.")

    humidity = response['main']['humidity']
    humidity = int(humidity)
    humidity = str('"' + str(humidity) + '%"')
    print('This is the humidity is ' + str(humidity))

    for item2 in response['weather']:
        current_weather = item2['id']
        if current_weather == '801' or '802' or '800':  # good weather for swimming
            swim_or_not = True

    try:
        warning = response['alerts']
        print(warning)
        swim_or_not = False
    except KeyError:
        print("No weather alerts in your local area where found.")


def get_forcast(city_name, country_name, api_key):
    url2 = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name},{country_name}&appid={api_key}&units=metric"
    response2 = requests.get(url2).json()
    print(response2)
    feels_like_3_hour = round(response2['list'][0]["main"]["feels_like"])
    print(feels_like_3_hour)


try:
    get_forcast(city_name, country_name, api_key)
    get_weather(city_name, country_name, api_key)
except TypeError:
    print('Sorry something went wrong, error code: TypeError')


# for actually deciding what pool temp to set the heater at

# if preferred_temp = 'normal'
