import os
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

mcp = FastMCP("WeatherServer")


@mcp.tool()
def get_current_weather(city: str) -> dict:
    """
    Get the current real-time weather for a given city using WeatherAPI.
    Returns temperature (Celsius), weather condition, humidity, and wind speed.
    """
    try:
        url = "https://api.weatherapi.com/v1/current.json"
        params = {
            "key": WEATHER_API_KEY,
            "q": city
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data["current"]
        location = data["location"]

        return {
            "city": location["name"],
            "country": location["country"],
            "region": location["region"],
            "temperature_c": current["temp_c"],
            "feels_like_c": current["feelslike_c"],
            "condition": current["condition"]["text"],
            "humidity_percent": current["humidity"],
            "wind_kph": current["wind_kph"],
            "wind_direction": current["wind_dir"],
            "visibility_km": current["vis_km"],
            "uv_index": current["uv"],
            "last_updated": current["last_updated"]
        }

    except requests.exceptions.HTTPError as e:
        return {"error": f"City '{city}' not found or API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}


@mcp.tool()
def get_weather_forecast(city: str, days: int = 3) -> dict:
    """
    Get a multi-day weather forecast for a given city.
    days: number of forecast days (1 to 3).
    """
    try:
        days = max(1, min(days, 3))  # clamp between 1 and 3
        url = "https://api.weatherapi.com/v1/forecast.json"
        params = {
            "key": WEATHER_API_KEY,
            "q": city,
            "days": days
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        location = data["location"]
        forecast_days = data["forecast"]["forecastday"]

        result = {
            "city": location["name"],
            "country": location["country"],
            "forecast": []
        }

        for day in forecast_days:
            result["forecast"].append({
                "date": day["date"],
                "max_temp_c": day["day"]["maxtemp_c"],
                "min_temp_c": day["day"]["mintemp_c"],
                "avg_temp_c": day["day"]["avgtemp_c"],
                "condition": day["day"]["condition"]["text"],
                "chance_of_rain_percent": day["day"]["daily_chance_of_rain"],
                "total_rain_mm": day["day"]["totalprecip_mm"],
                "avg_humidity": day["day"]["avghumidity"],
                "max_wind_kph": day["day"]["maxwind_kph"]
            })

        return result

    except requests.exceptions.HTTPError as e:
        return {"error": f"City '{city}' not found or API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to fetch forecast: {str(e)}"}


if __name__ == "__main__":
    mcp.run()
