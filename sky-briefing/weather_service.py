"""
Talks to the Open-Meteo API (free, no key needed). Shared by app.py (the
web app) and send_daily_alerts.py (the email script), so there's one place
that knows how to fetch weather.
"""

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def geocode_city(city_name):
    """Turn a city name into (latitude, longitude, display_name) or None."""
    resp = requests.get(GEOCODE_URL, params={"name": city_name, "count": 1}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results")
    if not results:
        return None
    place = results[0]
    display_name = place["name"]
    if place.get("admin1"):
        display_name += f", {place['admin1']}"
    if place.get("country"):
        display_name += f", {place['country']}"
    return place["latitude"], place["longitude"], display_name


def fetch_weather(lat, lon):
    """Get current conditions + 5-day daily summary for a location."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,precipitation,weather_code,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
        "timezone": "auto",
        "forecast_days": 5,
    }
    resp = requests.get(FORECAST_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_conditions_for_city(city_name):
    """
    High-level helper: city name in, structured current+forecast data out.
    Returns None if the city can't be found.
    """
    from outfit_core import recommend_outfit, describe_weather_code

    location = geocode_city(city_name)
    if location is None:
        return None

    lat, lon, display_name = location
    weather = fetch_weather(lat, lon)

    current_raw = weather["current"]
    daily = weather["daily"]

    outfit = recommend_outfit(
        temp_c=current_raw["temperature_2m"],
        precipitation_prob=daily["precipitation_probability_max"][0] or 0,
        wind_kmh=current_raw["wind_speed_10m"],
        weather_code=current_raw["weather_code"],
    )
    condition_label, _ = describe_weather_code(current_raw["weather_code"])

    current = {
        "temp": round(current_raw["temperature_2m"]),
        "condition": condition_label,
        "wind": round(current_raw["wind_speed_10m"]),
        "rain_chance": daily["precipitation_probability_max"][0] or 0,
    }

    forecast = []
    for i in range(len(daily["time"])):
        label, _ = describe_weather_code(daily["weather_code"][i])
        forecast.append({
            "date": daily["time"][i],
            "high": round(daily["temperature_2m_max"][i]),
            "low": round(daily["temperature_2m_min"][i]),
            "rain_chance": daily["precipitation_probability_max"][i],
            "condition": label,
        })

    return {
        "city": display_name,
        "current": current,
        "outfit": outfit,
        "forecast": forecast,
    }
