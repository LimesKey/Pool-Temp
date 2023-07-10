from time import localtime, strftime
from math import log


def calculate_temp(
        time2: str,
        units: str,
        current_temp: float,
        humidity: int,
        feels_like: float,
        feels_like_3_hour: float,
        humidity_in_3_hour: int,
        sunset_unix: float | int
    ) -> tuple[str, int]:
    # include documentation here.
    heater_temp = current_temp
    calcuate_sunrise_comparison2: str = strftime(
            "%H%M", localtime(sunset_unix)
        )
    dew_point = dew_point_calc(heater_temp, humidity)

    while dew_point >= heater_temp:
        dew_point = dew_point_calc(heater_temp, humidity)
        heater_temp -= 1

    if time2 > calcuate_sunrise_comparison2:
        return (
                (
                    "Its currently dark outside so"
                    " I wouldn't recommend swimming"
                ),
                0
            )

    if units.lower() == "f":
        current_temp *= 1.8 + 32
        feels_like *= 1.8 + 32
        feels_like_3_hour *= 1.8 + 32

    

def dew_point_calc(
        temp: float,
        humidity: int
    ) -> float:
    # include documentation here.

    alpha = ((a * temp) / (b + temp)) + math.log(humidity/100.0)
    dew_point = (b * alpha) / (a - alpha)
    dew_point = round(dew_point, 1)
    return dew_point
