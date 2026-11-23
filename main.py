from src.weather_api import get_weather
from src.alert_system import generate_alerts
from src.report_generator import (
    save_forecast_csv,
    save_forecast_chart,
    save_text_report,
)


def main():
    print("\nWeather Forecast & Alert Application")
    print("-------------------------------------")

    city = input("Enter city (default: Kolkata): ").strip() or "Kolkata"
    mode_input = input("Use live API? Type y for live, anything else for simulation: ")
    mode = "Live API" if mode_input.strip().lower() == "y" else "Simulation"

    try:
        weather = get_weather(city, mode)
        current = weather["current"]

        print(f"\nWeather in {weather['city']}, {weather['country']}")
        print(f"Temperature: {current['temperature']}°C")
        print(f"Feels like: {current['feels_like']}°C")
        print(f"Humidity: {current['humidity']}%")
        print(f"Wind speed: {current['wind_speed']} m/s")
        print(f"Conditions: {current['description']}")

        print("\nForecast")
        for day in weather["forecast"]:
            print(
                f"{day['date']}: {day['min_temp']}°C to {day['max_temp']}°C, "
                f"rain chance {day['rain_probability']}%"
            )

        alerts = generate_alerts(weather)
        print("\nAlerts")
        for alert in alerts:
            print(f"- {alert}")

        csv_path = save_forecast_csv(weather)
        chart_path = save_forecast_chart(weather)
        report_path = save_text_report(weather, alerts)

        print("\nFiles created:")
        print(f"CSV: {csv_path}")
        print(f"Chart: {chart_path}")
        print(f"Report: {report_path}")

    except Exception as error:
        print(f"\nCould not load weather data: {error}")


if __name__ == "__main__":
    main()