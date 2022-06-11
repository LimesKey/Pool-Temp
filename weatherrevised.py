import requests
import math
import time

# intro
print("This program is for finding the best pool temperature to set your heater at to save the most amount of money "
      "whilst still having a good temperature pool.")

city_name = str(input("What City or Town do you live in?\n")).lower()
country_name = str(input("What country do you live in?\n")).upper()
api_key = input("What's your ApiKey for OpenWeatherMap?\n").lower()

time2 = time.strftime("%X", time.localtime())  # get time
if api_key == '':
    api_key = ""

swim_or_not = False
pool_temp_normal = 29

if city_name == "milton":
    city_name = "Oakville"


def get_weather(city_name, country_name, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}, {country_name}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if 'cod' in response and response['cod'] == '404':
        print('You can get this error when you specified the wrong city name, ZIP-code or city ID. For your '
              'reference, this list contains City name, City ID, Geographical coordinates of the city (lon, lat), '
              'Zoom, etc. We are sorry.')
    else:
        global current_temp
        global feels_like
        global humidity
        global current_weather
        global swim_or_not
        global units
        if response['sys']['country'] == 'US':
            units = 'F'
        else:
            units = 'C'
        current_temp = round(response['main']['temp'])  # get temp
        print(f'The current temp is {current_temp}.')

        feels_like = response['main']["feels_like"]  # get feel like
        feels_like = round(feels_like)
        print(f"This is feels like {feels_like}.")

        humidity = response['main']['humidity']
        humidity = round(humidity)
        print(f'The humidity is {humidity}%.')

        global partial_swim
        partial_swim = False

        for item2 in response['weather']:
            current_weather = item2['id']
            if current_weather == '801' or '802' or '800':  # good weather for swimming
                partial_swim = False
            else:
                partial_swim = True

        global warning
        try:
            warning = response['alerts']
            swim_or_not = True
        except KeyError:
            pass
        if current_temp < 10:
            partial_swim = True
        if current_temp < 0:
            swim_or_not = True


def get_forcast(city_name, country_name, api_key):
    url2 = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name},{country_name}&appid={api_key}&units=metric"
    response2 = requests.get(url2).json()
    print(response2)
    if 'cod' in response2 and response2['cod'] == '404':
        pass
    else:
        global feels_like_3_hour
        feels_like_3_hour = round(response2['list'][0]["main"]["feels_like"])
        print(f'The air temp in 3 hours will be {feels_like_3_hour}c')
        global humidity_in_3_hour
        humidity_in_3_hour = round(response2['list'][0]['main']['humidity'])
        print(f'The humidity in 3 hours will be {humidity_in_3_hour}.')


try:
    get_forcast(city_name, country_name, api_key)
    get_weather(city_name, country_name, api_key)
except TypeError:
    print(f'Sorry something went wrong, error code: {TypeError}')


# for actually deciding what pool temp to set the heater at
def calculate_temp(current_temp, humidity, feels_like_3_hour, feels_like, pool_temp_normal, humidity_in_3_hour, swim_or_not, partial_swim):
    if units == 'F':
        current_temp *= 1.8 + 32
        feels_like *= 1.8 + 32
        feels_like_3_hour *= 1.8 + 32

    if feels_like_3_hour > current_temp and humidity_in_3_hour < humidity:
        pool_temp_normal += 0

    if feels_like_3_hour > current_temp and humidity_in_3_hour > humidity:
        pool_temp_normal -= 1

    if feels_like_3_hour < current_temp and humidity > humidity_in_3_hour:
        pool_temp_normal += 1
        partial_swim = True


try:
    calculate_temp(current_temp, humidity, feels_like_3_hour, feels_like, pool_temp_normal, humidity_in_3_hour, swim_or_not, partial_swim)
except TypeError:
    print(f'Sorry something went wrong, error code: {TypeError}')
if units == 'F':
    pool_temp_normal *= 1.8 + 32

if swim_or_not:
    print(f"I cannot give you a temperature to set your pool heater at because of dangerous weather concerns in your area. The "
          f"weather concern is {warning}.")
elif partial_swim:
    print(f'Your suggested pool heater temperature is {pool_temp_normal}{units} but I wouldn\'t recommend you to swim at this time.')
else:
    print(f'Your suggested pool heater temperature is {pool_temp_normal}{units}. There where no weather concerns in '
          f'your area.')
