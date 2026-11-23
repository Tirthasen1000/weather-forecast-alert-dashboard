import streamlit as st

from src.weather_api import get_weather
from src.alert_system import generate_alerts
from src.weather_analysis import forecast_to_dataframe
from src.report_generator import (
    save_forecast_csv,
    save_forecast_chart,
    save_text_report,
)

st.set_page_config(
    page_title="Weather Forecast & Alerts",
    page_icon="🌦️",
    layout="wide",
)

st.title("🌦️ Weather Forecast & Alert Application")
st.caption("Check current weather, view the forecast, and review weather alerts.")

with st.sidebar:
    st.header("Settings")
    city = st.text_input("City", value="Kolkata")
    mode = st.radio("Data source", ["Simulation", "Live API"])
    load_button = st.button("Load weather", type="primary")

if "weather_data" not in st.session_state:
    st.session_state.weather_data = None

if load_button:
    try:
        st.session_state.weather_data = get_weather(city.strip() or "Kolkata", mode)
        st.session_state.weather_error = None
    except Exception as error:
        st.session_state.weather_data = None
        st.session_state.weather_error = str(error)

if st.session_state.get("weather_error"):
    st.error(st.session_state.weather_error)

weather = st.session_state.weather_data

if weather:
    current = weather["current"]
    forecast_df = forecast_to_dataframe(weather)
    alerts = generate_alerts(weather)

    st.subheader(f"{weather['city']}, {weather['country']}")
    st.write(f"Current conditions: {current['description'].title()}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Temperature", f"{current['temperature']} °C")
    col2.metric("Feels like", f"{current['feels_like']} °C")
    col3.metric("Humidity", f"{current['humidity']}%")
    col4.metric("Wind speed", f"{current['wind_speed']} m/s")

    st.subheader("5-Day Forecast")
    st.dataframe(forecast_df, use_container_width=True, hide_index=True)

    chart_data = forecast_df.set_index("date")[["min_temp", "max_temp"]]
    st.line_chart(chart_data)

    st.subheader("Weather Alerts")
    for alert in alerts:
        if "No weather alerts" in alert:
            st.success(alert)
        else:
            st.warning(alert)

    st.subheader("Download Reports")
    csv_path = save_forecast_csv(weather)
    chart_path = save_forecast_chart(weather)
    report_path = save_text_report(weather, alerts)

    with open(csv_path, "rb") as file:
        st.download_button(
            "Download forecast CSV",
            data=file,
            file_name="weather_forecast.csv",
            mime="text/csv",
        )

    with open(chart_path, "rb") as file:
        st.download_button(
            "Download forecast chart",
            data=file,
            file_name="forecast_chart.png",
            mime="image/png",
        )

    with open(report_path, "rb") as file:
        st.download_button(
            "Download weather report",
            data=file,
            file_name="weather_report.txt",
            mime="text/plain",
        )
else:
    st.info("Choose a data source in the sidebar and click **Load weather**.")