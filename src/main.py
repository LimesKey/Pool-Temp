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
    pool_temp_normal: float = 29.0

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
        atnighttrue, atnight = calculate_temp(
                time2,
                units,
                current_temp,
                humidity,
                feels_like,
                feels_like_3_hour,
                pool_temp_normal,
                humidity_in_3_hour,
                sunset_unix
            )
    except TypeError as Err:
        print(f"Sorry something went wrong, error code: {Err}")
    except KeyError as Err:
        print(f"Sorry something went wrong, error code {Err}.")
    else:
        if units.lower() == "F":
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
                    " recommend you to swim at this "
                )
        else:
            print(
                "Your suggested pool heater temperature is "
                f"{pool_temp_normal}{units}, there where no"
                " weather concerns in your area."
            )


if __name__ == "__main__":
    main()
