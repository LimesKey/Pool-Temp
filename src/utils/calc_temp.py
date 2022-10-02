from time import localtime, strftime


def calculate_temp(
        time2: int,
        units: str,
        current_temp: int,
        humidity: int,
        feels_like_3_hour: int,
        feels_like: int,
        pool_temp_normal: int,
        humidity_in_3_hour: int,
        sunset_unix: float | int
    ) -> tuple[bool, str]:
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
    calcuate_sunrise_comparison2 = strftime(
            "%H%M", localtime(sunset_unix)
        )
    atnighttrue = False
    atnight = ""
    if time2 > calcuate_sunrise_comparison2:
        atnight = (
                "Its currently dark outside so I wouldn\"t recommend swimming"
            )
        atnighttrue = True
    return atnighttrue, atnight
