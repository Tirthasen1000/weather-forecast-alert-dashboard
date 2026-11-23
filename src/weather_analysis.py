import pandas as pd


def forecast_to_dataframe(weather_data):
    """Convert the forecast list into a DataFrame for tables and charts."""
    return pd.DataFrame(weather_data["forecast"])


def get_temperature_summary(weather_data):
    current = weather_data["current"]
    forecast_df = forecast_to_dataframe(weather_data)

    return {
        "current_temp": current["temperature"],
        "feels_like": current["feels_like"],
        "humidity": current["humidity"],
        "wind_speed": current["wind_speed"],
        "forecast_high": forecast_df["max_temp"].max(),
        "forecast_low": forecast_df["min_temp"].min(),
    }