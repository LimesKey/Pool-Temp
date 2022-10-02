from typing import Any

from requests import get


def get_forcast(
        city_name: str,
        country_name: str,
        api_key: str
    ) -> None:
    url2: str = (
            "https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city_name},{country_name}&appid={api_key}&units=metric"
        )
    response2: dict[str | Any] = get(url2).json()
    if "cod" in response2 and response2["cod"] != "404" or "404":
        global feels_like_3_hour
        feels_like_3_hour: int = round(response2["list"][0]["main"]["feels_like"])
        print(f"The air temp in 3 hours will be {feels_like_3_hour}c")
        global humidity_in_3_hour
        humidity_in_3_hour: int = round(response2["list"][0]["main"]["humidity"])
        print(f"The humidity in 3 hours will be {humidity_in_3_hour}.")
    else:
        print("party")
