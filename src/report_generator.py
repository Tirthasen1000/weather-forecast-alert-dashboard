from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"
REPORT_DIR = PROJECT_ROOT / "reports"


def create_output_folders():
    OUTPUT_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)


def save_forecast_csv(weather_data):
    create_output_folders()
    dataframe = pd.DataFrame(weather_data["forecast"])
    file_path = OUTPUT_DIR / "weather_forecast.csv"
    dataframe.to_csv(file_path, index=False)
    return file_path


def save_forecast_chart(weather_data):
    create_output_folders()
    dataframe = pd.DataFrame(weather_data["forecast"])

    chart_path = OUTPUT_DIR / "forecast_chart.png"

    plt.figure(figsize=(10, 5))
    plt.plot(
        dataframe["date"],
        dataframe["max_temp"],
        marker="o",
        label="Maximum temperature",
    )
    plt.plot(
        dataframe["date"],
        dataframe["min_temp"],
        marker="o",
        label="Minimum temperature",
    )
    plt.title(f"5-Day Temperature Forecast — {weather_data['city']}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=30)
    plt.legend()
    plt.tight_layout()
    plt.savefig(chart_path, dpi=150)
    plt.close()

    return chart_path


def save_text_report(weather_data, alerts):
    create_output_folders()

    current = weather_data["current"]
    report_path = REPORT_DIR / "weather_report.txt"

    lines = [
        f"Weather Report: {weather_data['city']}, {weather_data['country']}",
        "",
        "Current conditions",
        f"Temperature: {current['temperature']}°C",
        f"Feels like: {current['feels_like']}°C",
        f"Humidity: {current['humidity']}%",
        f"Wind speed: {current['wind_speed']} m/s",
        f"Conditions: {current['description']}",
        "",
        "Forecast",
    ]

    for day in weather_data["forecast"]:
        lines.append(
            f"{day['date']}: {day['min_temp']}°C to {day['max_temp']}°C, "
            f"rain chance {day['rain_probability']}%"
        )

    lines.extend(["", "Alerts"])
    lines.extend(f"- {alert}" for alert in alerts)

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path