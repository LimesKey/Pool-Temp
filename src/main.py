from time import strftime, localtime

from src.utils.calc_temp import calculate_temp # type: ignore
from src.utils.get_forecast import get_forcast # type: ignore
from src.utils.get_weather import get_weather # type: ignore


def main() -> None:
    # intro
    print(
        (
            "This program is for finding the best pool temperature"
            " to set your heater at to save the most amount of money"
            " whilst still having a good temperature pool."
        )
    )

    city_name: str = input("What City or Town do you live in?\n").lower()
    country_name: str = input("What country do you live in?\n").upper()
    api_key: str = input("What's your ApiKey for OpenWeatherMap?\n").lower()

    time2: str = strftime("%H%M", localtime())  # get time

    swim_or_not: bool = False

    if city_name == "milton":
        city_name = "Oakville"

    try:
        (
            feels_like_3_hour,
            humidity_in_3_hour
        ) = get_forcast(
                city_name,
                country_name,
                api_key
            )

        (
            current_temp,
            feels_like,
            humidity,
            current_temp,
            swim_or_not,
            units,
            sunset_unix,
            warning,
            partial_swim
        ) = get_weather(
                city_name,
                country_name,
                api_key
            )

    except TypeError as Err:
        print(f"Sorry something went wrong, error code: {Err}")
    except KeyError as Err:
        print(f"Sorry something went wrong, error code {Err}.")
    else:
        if units.lower() == "F":
            pool_temp_normal *= 1.8 + 32

        print(
            (
                f"The current temp is {current_temp}."
                f"\nThis is feels like {feels_like}."
                f"\nThe humidity is {humidity}%."
                "The air temp in 3 hours will be"
                f"{feels_like_3_hour}c\n"
                "The humidity in 3 hours will"
                f"be {humidity_in_3_hour}."
            )
        )

if __name__ == "__main__":
    main()
