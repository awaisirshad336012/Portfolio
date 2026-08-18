"""
Core logic for the Sky Briefing outfit recommender.
No Flask, no input()/print() here - just pure functions, so they're easy to unit test.
"""

# WMO weather codes -> human readable label + a short icon-ish tag
# (Open-Meteo uses the WMO weather interpretation codes)
WEATHER_CODES = {
    0: ("Clear sky", "clear"),
    1: ("Mainly clear", "clear"),
    2: ("Partly cloudy", "cloudy"),
    3: ("Overcast", "cloudy"),
    45: ("Fog", "fog"),
    48: ("Depositing rime fog", "fog"),
    51: ("Light drizzle", "rain"),
    53: ("Moderate drizzle", "rain"),
    55: ("Dense drizzle", "rain"),
    61: ("Slight rain", "rain"),
    63: ("Moderate rain", "rain"),
    65: ("Heavy rain", "rain"),
    71: ("Slight snow", "snow"),
    73: ("Moderate snow", "snow"),
    75: ("Heavy snow", "snow"),
    80: ("Rain showers", "rain"),
    81: ("Moderate rain showers", "rain"),
    82: ("Violent rain showers", "rain"),
    95: ("Thunderstorm", "storm"),
    96: ("Thunderstorm with hail", "storm"),
    99: ("Thunderstorm with heavy hail", "storm"),
}


def describe_weather_code(code):
    """Turn a WMO weather code into a (label, category) tuple."""
    return WEATHER_CODES.get(code, ("Unknown", "clear"))


def temperature_band(temp_c):
    """Classify temperature in Celsius into a simple band."""
    if temp_c <= 0:
        return "freezing"
    if temp_c <= 10:
        return "cold"
    if temp_c <= 18:
        return "cool"
    if temp_c <= 25:
        return "mild"
    if temp_c <= 32:
        return "warm"
    return "hot"


def recommend_outfit(temp_c, precipitation_prob, wind_kmh, weather_code):
    """
    Build an outfit recommendation from current conditions.

    temp_c: current temperature in Celsius
    precipitation_prob: chance of rain, 0-100
    wind_kmh: wind speed in km/h
    weather_code: WMO weather code from the API

    Returns a dict with: verdict (headline advice), layers (list of clothing
    items), and warnings (list of short heads-up messages).
    """
    band = temperature_band(temp_c)
    _, category = describe_weather_code(weather_code)

    layers = []
    warnings = []

    if band == "freezing":
        layers += ["thermal base layer", "heavy coat", "gloves", "warm hat"]
    elif band == "cold":
        layers += ["sweater", "jacket", "scarf"]
    elif band == "cool":
        layers += ["light jacket or hoodie"]
    elif band == "mild":
        layers += ["long sleeve shirt"]
    elif band == "warm":
        layers += ["t-shirt", "light trousers or shorts"]
    else:  # hot
        layers += ["breathable t-shirt", "shorts", "sunglasses"]
        warnings.append("It's hot — stay hydrated")

    if precipitation_prob >= 60 or category == "rain":
        layers.append("umbrella")
        layers.append("waterproof shoes")
        warnings.append("High chance of rain")
    elif precipitation_prob >= 30:
        layers.append("umbrella (just in case)")

    if category == "storm":
        warnings.append("Thunderstorms expected — consider staying indoors")

    if category == "snow":
        layers.append("waterproof boots")
        warnings.append("Snow expected — watch your step")

    if wind_kmh >= 30:
        layers.append("windbreaker")
        warnings.append("Windy conditions")

    if category == "fog":
        warnings.append("Foggy — take care if you're driving")

    # Headline verdict, one line
    if warnings:
        verdict = f"{band.capitalize()} and {category} — {warnings[0].lower()}"
    else:
        verdict = f"{band.capitalize()} and {category} out there — dress accordingly"

    return {
        "verdict": verdict,
        "layers": layers,
        "warnings": warnings,
        "band": band,
        "category": category,
    }
