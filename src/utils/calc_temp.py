from time import localtime, strftime


def calculate_temp(
        time2: str,
        units: str,
        current_temp: float,
        humidity: int,
        feels_like: float,
        feels_like_3_hour: float,
        pool_temp_normal: int,
        humidity_in_3_hour: int,
        sunset_unix: float | int
    ) -> tuple[str, bool]:
    # include documentation here.

    if units.lower() == "f":
        current_temp *= 1.8 + 32
        feels_like *= 1.8 + 32
        feels_like_3_hour *= 1.8 + 32

    if (
            (feels_like_3_hour > current_temp)
            and (humidity_in_3_hour < humidity)
        ):
        pool_temp_normal += 0
    elif (
            (feels_like_3_hour > current_temp)
            and (humidity_in_3_hour > humidity)
        ):
        pool_temp_normal -= 1
    elif (
            (feels_like_3_hour < current_temp)
            and (humidity > humidity_in_3_hour)
        ):
        pool_temp_normal += 1

    calcuate_sunrise_comparison2: str = strftime(
            "%H%M", localtime(sunset_unix)
        )

    if time2 > calcuate_sunrise_comparison2:
        return (
                (
                    "Its currently dark outside so"
                    " I wouldn't recommend swimming"
                ),
                True
            )

    return "", False
