from time import localtime, strftime
from typing import Any

from requests import get


def get_weather(
        city_name: str,
        country_name: str,
        api_key: str
    ) -> None:
    # include documentation

    url: str = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city_name}, {country_name}&appid={api_key}&units=metric"
        )

    response: Any = get(url).json()
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

        if response["sys"]["country"].lower() == "US":
            units: str = "F"
        else:
            units = "C"

        sunset_unix: str = response["sys"]["sunset"]

        # %I is for 24 hour time, %p is for AM/PM time
        sunset: str = strftime(
                "%I:%M %p", localtime(int(sunset_unix))
            ).lstrip("0")
        current_temp: int = round(response["main"]["temp"])

        feels_like: int = response["main"]["feels_like"]  # get feel like
        feels_like: int = round(feels_like)

        humidity: int = round(response["main"]["humidity"])

        partial_swim: bool = False

        for item2 in response["weather"]:
            current_weather: int = item2["id"]
            if current_weather in [801, 802, 800]:  # good weather for swimming
                partial_swim = False
            else:
                partial_swim = True

        print(
            (
                f"The current temp is {current_temp}."
                f"\nThis is feels like {feels_like}."
                f"\nThe humidity is {humidity}%."
            )
        )

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

    return (
        current_temp,
        feels_like,
        humidity,
        current_weather,
        current_temp,
        swim_or_not,
        units,
        sunset,
        sunset_unix,
        warning,
        partial_swim
    )
