from time import localtime, strftime
from typing import Any

from requests import get


def get_weather(
        city_name: str,
        country_name: str,
        api_key: str
    ) -> tuple[
        int,
        int,
        int,
        int,
        bool,
        str,
        str,
        str,
        bool
    ]:
    # include documentation

    url: str = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city_name}, {country_name}&appid={api_key}&units=metric"
        )

    response: Any = get(url).json()
    for _ in range(3):
        try:
            if "cod" in response and response["cod"] == "401":
                api_key = input(
                        (
                            "Your API Key was incorrect, please "
                            "enter it again. You may need to wait"
                            " a few hours for it to activate."
                        )
                    ).lower()
            elif "cod" in response and response["cod"] == "404":
                print(
                    (
                        "You can get this error when you specified the "
                        "wrong city name, ZIP-code or city ID. For your"
                        " reference this list contains City name, City "
                        "ID, Geographical coordinates of the city (lon,"
                        " lat), Zoom, etc. We are sorry."
                    )
                )
            else:
                break
        except (ConnectionError, ConnectionRefusedError):
            continue

        raise SystemExit

    if response["sys"]["country"].lower() == "US":
        units: str = "F"
    else:
        units = "C"

    sunset_unix: str = response["sys"]["sunset"]
    current_temp: int = round(response["main"]["temp"])
    feels_like: int = response["main"]["feels_like"]  # get feel like
    feels_like = round(feels_like)
    humidity: int = round(response["main"]["humidity"])

    partial_swim: bool = False

    for item2 in response["weather"]:
        current_weather: int = item2["id"]
        if current_weather in [801, 802, 800]:  # good weather for swimming
            partial_swim = False
        else:
            partial_swim = True

    swim_or_not: bool = True
    try:
        warning: str = response["alerts"]
    except KeyError:
        warning: str = None

    if current_temp < 10:
        partial_swim = True
    elif current_temp < 0:
        swim_or_not = True
    elif humidity > 90:
        partial_swim = True

    return (
        current_temp,
        feels_like,
        humidity,
        current_temp,
        swim_or_not,
        units,
        sunset_unix,
        warning,
        partial_swim
    )
