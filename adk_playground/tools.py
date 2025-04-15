import datetime

import openmeteo_requests
import pandas as pd
import requests_cache
from geopy import geocoders
from geopy.geocoders import Nominatim
from retry_requests import retry

from adk_playground.config import cfg

loc = Nominatim(user_agent="Geopy Library")
cache_session = requests_cache.CachedSession(".cache", expire_after=cfg.cache_expiry)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

current_weather_fields = [
    "temperature_2m",
    "precipitation",
    "relative_humidity_2m",
    "rain",
    "weather_code",
    "wind_speed_10m",
]
current_weather_fields_dict = {
    field: i for i, field in enumerate(current_weather_fields)
}


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city using OpenWeatherMap API.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    try:
        # Configure the OWM instance
        getLoc = loc.geocode(city)
        assert getLoc, f"Failed to get location for city: {city}"
        assert (
            getLoc.latitude and getLoc.longitude
        ), f"Failed to get latitude and longitude for city: {city}"
        latitude, longitude = getLoc.latitude, getLoc.longitude
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation_probability",
                "apparent_temperature",
                "precipitation",
                "rain",
                "showers",
                "snowfall",
                "weather_code",
                "wind_speed_10m",
                "wind_speed_80m",
            ],
            "current": current_weather_fields,
        }
        responses = openmeteo.weather_api(cfg.open_meteo_api_url, params=params)
        return {
            "status": "success",
            "result": responses,
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to get weather information: {str(e)}",
        }


def get_weather_current_str(city: str) -> str:
    """Retrieves the current weather report for a specified city using OpenWeatherMap API.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        str: weather report as markdownor error msg
    """
    weather = get_weather(city)
    if weather["status"] == "success":
        if len(weather["result"]) > 0:
            result = weather["result"][0]
            current = result.Current()
            current_temperature_2m = current.Variables(
                current_weather_fields_dict["temperature_2m"]
            ).Value()
            current_precipitation = current.Variables(
                current_weather_fields_dict["precipitation"]
            ).Value()
            current_relative_humidity_2m = current.Variables(
                current_weather_fields_dict["relative_humidity_2m"]
            ).Value()
            current_rain = current.Variables(
                current_weather_fields_dict["rain"]
            ).Value()
            current_weather_code = current.Variables(
                current_weather_fields_dict["weather_code"]
            ).Value()
            current_wind_speed_10m = current.Variables(
                current_weather_fields_dict["wind_speed_10m"]
            ).Value()

            return f"""
# Current weather in {city}:

Temperature: {current_temperature_2m}°C
Precipitation: {current_precipitation} mm
Relative humidity: {current_relative_humidity_2m}%
Rain: {current_rain} mm
Weather code: {current_weather_code}
Wind speed: {current_wind_speed_10m} m/s
"""
        else:
            return "No weather data found"
    else:
        return weather["error_message"]


def get_weather_forecast_as_str(city: str) -> str:
    """Retrieves the future weather forecast for the following 7 days for a specified city using OpenWeatherMap API.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        str: table with detailed weather forecast for the following 7 days and result or error msg.
    """
    weather = get_weather(city)
    if weather["status"] == "success":
        if len(weather["result"]) > 0:
            result = weather["result"][0]

            hourly = result.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
            hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
            hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
            hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
            hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()
            hourly_rain = hourly.Variables(5).ValuesAsNumpy()
            hourly_showers = hourly.Variables(6).ValuesAsNumpy()
            hourly_snowfall = hourly.Variables(7).ValuesAsNumpy()
            hourly_weather_code = hourly.Variables(8).ValuesAsNumpy()
            hourly_wind_speed_10m = hourly.Variables(9).ValuesAsNumpy()
            hourly_wind_speed_80m = hourly.Variables(10).ValuesAsNumpy()

            hourly_data = {
                "date": pd.date_range(
                    start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                    end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=hourly.Interval()),
                    inclusive="left",
                )
            }

            hourly_data["temperature_2m"] = hourly_temperature_2m
            hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
            hourly_data["precipitation_probability"] = hourly_precipitation_probability
            hourly_data["apparent_temperature"] = hourly_apparent_temperature
            hourly_data["precipitation"] = hourly_precipitation
            hourly_data["rain"] = hourly_rain
            hourly_data["showers"] = hourly_showers
            hourly_data["snowfall"] = hourly_snowfall
            hourly_data["weather_code"] = hourly_weather_code
            hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
            hourly_data["wind_speed_80m"] = hourly_wind_speed_80m

            hourly_dataframe = pd.DataFrame(data=hourly_data)

            return f"""
# Weather forecast for the following 7 days in {city}:

{hourly_dataframe.to_markdown()}
"""
        else:
            return "No weather data found"
    else:
        return weather["error_message"]


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    g = geocoders.GoogleV3(api_key=cfg.geo_coder_api_key)
    place, (lat, lng) = g.geocode(city)

    if not place:
        return {
            "status": "error",
            "error_message": (f"Sorry, I don't have timezone information for {city}."),
        }

    tz = g.reverse_timezone((lat, lng))
    now = datetime.datetime.now(tz.pytz_timezone)
    report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    return {"status": "success", "report": report}
