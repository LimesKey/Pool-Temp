import requests
import time


# intro
print(
    (
        "This program is for finding the best pool temperature"
        " to set your heater at to save the most amount of money"
        " whilst still having a good temperature pool."
    )
)

city_name = str(input("What City or Town do you live in?\n")).lower()
country_name = str(input("What country do you live in?\n")).upper()
api_key = input("What's your ApiKey for OpenWeatherMap?\n").lower()

time2 = time.strftime("%H%M", time.localtime())  # get time
if api_key == "":
    api_key = ""

swim_or_not = False
pool_temp_normal = 29

if city_name == "milton":
    city_name = "Oakville"


def get_weather(city_name, country_name, api_key):
    url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city_name}, {country_name}&appid={api_key}&units=metric"
        )
    response = requests.get(url).json()
    while "cod" in response and response["cod"] == "401":
        api_key = input(
                (
                    "Your API Key was incorrect, please enter it again. "
                    "You may need to wait a few hours for it to activate."
                )
            ).lower()
    if "cod" in response and response["cod"] == "404":
        print(
            (
                "You can get this error when you specified the wrong "
                "city name, ZIP-code or city ID. For your reference, this"
                " list contains City name, City ID, Geographical "
                "coordinates of the city (lon, lat), Zoom, etc. We are sorry."
            )
        )
    else:
        global current_temp
        global feels_like
        global humidity
        global current_weather
        global swim_or_not
        global units
        global sunset
        global sunset_unix
        if response["sys"]["country"] == "US":
            units = "F"
        else:
            units = "C"
        sunset_unix = response["sys"]["sunset"]
        sunset = time.strftime("%I:%M %p", time.localtime(int(sunset_unix)))  # %I is for 24 hour time, %p is for AM/PM time
        sunset = sunset.lstrip("0")  # strips the 0 in front of the hour
        current_temp = round(response["main"]["temp"])  # get temp
        print(f"The current temp is {current_temp}.")

        feels_like = response["main"]["feels_like"]  # get feel like
        feels_like = round(feels_like)
        print(f"This is feels like {feels_like}.")

        humidity = round(response["main"]["humidity"])
        print(f"The humidity is {humidity}%.")

        global partial_swim
        partial_swim = False

        for item2 in response["weather"]:
            current_weather = item2["id"]
            if current_weather in [801, 802, 800]:  # good weather for swimming
                partial_swim = False
            else:
                partial_swim = True

        global warning
        try:
            warning = response["alerts"]
            swim_or_not = True
        except KeyError:
            pass

        if current_temp < 10:
            partial_swim = True
        if current_temp < 0:
            swim_or_not = True
        if humidity > 90:
            partial_swim = True


def get_forcast(city_name, country_name, api_key):
    url2 = (
            "https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city_name},{country_name}&appid={api_key}&units=metric"
        )
    response2 = requests.get(url2).json()
    if "cod" in response2 and response2["cod"] != "404" or "404":
        global feels_like_3_hour
        feels_like_3_hour = round(response2["list"][0]["main"]["feels_like"])
        print(f"The air temp in 3 hours will be {feels_like_3_hour}c")
        global humidity_in_3_hour
        humidity_in_3_hour = round(response2["list"][0]["main"]["humidity"])
        print(f"The humidity in 3 hours will be {humidity_in_3_hour}.")
    else:
        print("party")

try:
    get_forcast(city_name, country_name, api_key)
    get_weather(city_name, country_name, api_key)
except TypeError:
    print(f"Sorry something went wrong, error code: {TypeError}")
except KeyError:
    print(f"Sorry something went wrong, error code {TypeError}.")


# for actually deciding what pool temp to set the heater at
def calculate_temp(
        current_temp,
        humidity,
        feels_like_3_hour,
        feels_like,
        pool_temp_normal,
        humidity_in_3_hour,
        swim_or_not, partial_swim,
        sunset,
        sunset_unix
    ):
    if units == "F":
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
    calcuate_sunrise_comparison2 = time.strftime(
            "%H%M", time.localtime(sunset_unix)
        )
    atnighttrue = False
    atnight = ""
    if time2 > calcuate_sunrise_comparison2:
        atnight = (
                "Its currently dark outside so I wouldn\"t recommend swimming"
            )
        atnighttrue = True
    return atnighttrue, atnight


try:
    atnighttrue, atnight = calculate_temp(
            current_temp,
            humidity,
            feels_like_3_hour,
            feels_like,
            pool_temp_normal,
            humidity_in_3_hour,
            swim_or_not,
            partial_swim,
            sunset,
            sunset_unix
        )
except TypeError:
    print(f"Sorry something went wrong, error code: {TypeError}")

if units == "F":
    pool_temp_normal *= 1.8 + 32

if swim_or_not:
    print(
        (
            "I cannot give you a temperature to set your pool"
            " heater at because of dangerous weather concerns "
            f"in your area. The weather concern is {warning}."
        )
    )
elif partial_swim:
    if atnighttrue:
        print(
            "Your suggested pool heater temperature "
            f"is {pool_temp_normal}{units} but {atnight}."
        )
    else:
        print(
            "Your suggested pool heater temperature is "
            f"{pool_temp_normal}{units}, but I wouldn't"
            " recommend you to swim at this time."
        )
else:
    print(
        "Your suggested pool heater temperature is "
        f"{pool_temp_normal}{units}, there where no"
        " weather concerns in your area."
    )
