def generate_alerts(weather_data):
    """Generate simple rule-based alerts from current conditions and forecast."""
    current = weather_data["current"]
    forecast = weather_data["forecast"]
    alerts = []

    if current["temperature"] >= 35:
        alerts.append("Heat alert: current temperature is 35°C or higher.")

    if current["humidity"] >= 85:
        alerts.append("High humidity alert: current humidity is 85% or higher.")

    for day in forecast:
        if day["rain_probability"] >= 70:
            alerts.append(
                f"Rain alert for {day['date']}: "
                f"{day['rain_probability']}% chance of rain."
            )

        if day["max_temp"] >= 38:
            alerts.append(
                f"High temperature alert for {day['date']}: "
                f"forecast high is {day['max_temp']}°C."
            )

    if not alerts:
        alerts.append("No weather alerts based on the current alert rules.")

    return alerts