from adk_playground.tools import get_weather, get_current_time
from adk_playground.config import cfg
from adk_playground.tools import current_weather_fields_dict, get_weather_current_str, get_weather_forecast_as_str 

def test_get_weather():
    weather = get_weather("London")
    assert weather["status"] == "success"
    assert weather["result"] is not None
    assert len(weather["result"]) > 0
    current = weather["result"][0].Current()
    current_temperature_2m = current.Variables(current_weather_fields_dict["temperature_2m"]).Value()
    current_precipitation = current.Variables(current_weather_fields_dict["precipitation"]).Value()
    current_relative_humidity_2m = current.Variables(current_weather_fields_dict["relative_humidity_2m"]).Value()
    current_rain = current.Variables(current_weather_fields_dict["rain"]).Value()
    current_weather_code = current.Variables(current_weather_fields_dict["weather_code"]).Value()
    current_wind_speed_10m = current.Variables(current_weather_fields_dict["wind_speed_10m"]).Value()
    assert current is not None, "Current weather data is not found"
    assert current_temperature_2m is not None, "Current temperature data is not found"
    assert current_precipitation is not None, "Current precipitation data is not found"
    assert current_relative_humidity_2m is not None, "Current relative humidity data is not found"
    assert current_rain is not None, "Current rain data is not found"
    assert current_weather_code is not None, "Current weather code data is not found"
    assert current_wind_speed_10m is not None, "Current wind speed data is not found"


def test_get_weather_current_str():
    weather = get_weather_current_str("London")
    assert weather is not None
    assert weather != "No weather data found"
    # Visualize the weather data
    with open("weather.md", "w") as f:
        f.write(weather)

def test_get_weather_forecast_as_str():
    weather = get_weather_forecast_as_str("London")
    assert weather is not None
    assert weather != "No weather data found"
    # Visualize the weather data
    with open("weather.md", "w") as f:
        f.write(weather)

def test_get_current_time():
    time = get_current_time("London")
    assert time is not None
    assert time != "No time data found"
    print(time)

