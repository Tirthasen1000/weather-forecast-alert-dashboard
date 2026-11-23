import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_FILE = PROJECT_ROOT / "data" / "sample_weather.json"
ENV_FILE = PROJECT_ROOT / ".env"

# Load the API key from the project's .env file
load_dotenv(dotenv_path=ENV_FILE)

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def load_sample_weather(city="Kolkata"):
    """Load sample weather data for a supported city."""
    with SAMPLE_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    cities = data["cities"]

    for city_name, weather_data in cities.items():
        if city_name.lower() == city.strip().lower():
            return weather_data

    available_cities = ", ".join(cities.keys())
    raise ValueError(
        f"Sample data is not available for '{city}'. "
        f"Available sample cities: {available_cities}"
    )


def get_live_weather(city):
    """Fetch current weather and a 5-day forecast for any supported city."""
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key or api_key == "your_actual_api_key_here":
        raise ValueError(
            "API key missing. Add your OpenWeatherMap key to the project's .env file."
        )

    params = {
        "q": city.strip(),
        "appid": api_key,
        "units": "metric",
    }

    # Fetch current weather
    current_response = requests.get(
        CURRENT_URL,
        params=params,
        timeout=15,
    )

    if current_response.status_code == 404:
        raise ValueError(
            f"City '{city}' was not found. Check the spelling and try again."
        )

    current_response.raise_for_status()
    current_data = current_response.json()

    current = current_data["main"]
    weather_info = current_data["weather"][0]

    current_weather = {
        "temperature": current["temp"],
        "feels_like": current["feels_like"],
        "humidity": current["humidity"],
        "pressure": current["pressure"],
        "wind_speed": current_data.get("wind", {}).get("speed", 0),
        "description": weather_info["description"],
        "icon": weather_info["icon"],
    }

    # Fetch the 5-day forecast (API readings are every 3 hours)
    forecast_response = requests.get(
        FORECAST_URL,
        params=params,
        timeout=15,
    )
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()

    daily_data = {}

    for item in forecast_data["list"]:
        date = item["dt_txt"].split(" ")[0]

        if date not in daily_data:
            daily_data[date] = {
                "temperatures": [],
                "humidity": [],
                "rain_probability": [],
                "descriptions": [],
            }

        daily_data[date]["temperatures"].append(item["main"]["temp"])
        daily_data[date]["humidity"].append(item["main"]["humidity"])
        daily_data[date]["rain_probability"].append(
            item.get("pop", 0) * 100
        )
        daily_data[date]["descriptions"].append(
            item["weather"][0]["description"]
        )

    forecast = []

    for date, values in list(daily_data.items())[:5]:
        forecast.append(
            {
                "date": date,
                "min_temp": round(min(values["temperatures"]), 1),
                "max_temp": round(max(values["temperatures"]), 1),
                "humidity": round(
                    sum(values["humidity"]) / len(values["humidity"])
                ),
                "rain_probability": round(max(values["rain_probability"])),
                "description": values["descriptions"][0],
            }
        )

    return {
        "city": current_data["name"],
        "country": current_data["sys"].get("country", ""),
        "current": current_weather,
        "forecast": forecast,
    }


def get_weather(city, mode="Simulation"):
    """Get live API data or local sample data based on the selected mode."""
    if mode == "Live API":
        return get_live_weather(city)

    return load_sample_weather(city)