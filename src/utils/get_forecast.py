from typing import Any

from requests import get


def get_forcast(
        city_name: str,
        country_name: str,
        api_key: str
    ) -> tuple[int, int] | None:
    # include documentation

    url2: str = (
            "https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city_name},{country_name}&appid={api_key}&units=metric"
        )
    response2: Any = get(url2).json()

    if (
            ("cod" in response2.lower())
            and (
                    (response2["cod"] != "404")
                    or (response2["cod"] == "404")
                )
        ):
        feels_like_3_hour: int = round(response2["list"][0]["main"]["feels_like"])
        humidity_in_3_hour: int = round(response2["list"][0]["main"]["humidity"])
        print(
            (
                f"The air temp in 3 hours will be {feels_like_3_hour}c\n"
                f"The humidity in 3 hours will be {humidity_in_3_hour}."
            )
        )
        return feels_like_3_hour, humidity_in_3_hour

    print("party")
