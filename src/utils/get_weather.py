from time import localtime, strftime
from typing import Any

from requests import get


def get_weather(
        city_name: str,
        country_name: str,
        api_key: str
    ) -> None:
    url: str = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city_name}, {country_name}&appid={api_key}&units=metric"
        )
    response: dict[str | Any] = get(url).json()
    while "cod" in response and response["cod"] == "401":
        api_key: str = input(
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
            units: str = "F"
        else:
            units = "C"
        sunset_unix: str = response["sys"]["sunset"]
        sunset: str = strftime("%I:%M %p", localtime(int(sunset_unix)))  # %I is for 24 hour time, %p is for AM/PM time
        sunset: str = sunset.lstrip("0")  # strips the 0 in front of the hour
        current_temp: int = round(response["main"]["temp"])  # get temp
        print(f"The current temp is {current_temp}.")

        feels_like: int = response["main"]["feels_like"]  # get feel like
        feels_like: int = round(feels_like)
        print(f"This is feels like {feels_like}.")

        humidity: int = round(response["main"]["humidity"])
        print(f"The humidity is {humidity}%.")

        global partial_swim
        partial_swim: bool = False

        for item2 in response["weather"]:
            current_weather: int = item2["id"]
            if current_weather in [801, 802, 800]:  # good weather for swimming
                partial_swim = False
            else:
                partial_swim = True

        global warning
        try:
            warning: str = response["alerts"]
            swim_or_not: bool = True
        except KeyError:
            pass

        if current_temp < 10:
            partial_swim = True
        if current_temp < 0:
            swim_or_not: bool = True
        if humidity > 90:
            partial_swim = True
