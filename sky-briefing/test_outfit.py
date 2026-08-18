"""
Unit tests for outfit_core.py.

Run with: pytest test_outfit.py -v
"""

from outfit_core import recommend_outfit, temperature_band, describe_weather_code


def test_temperature_band_freezing():
    assert temperature_band(-5) == "freezing"


def test_temperature_band_hot():
    assert temperature_band(35) == "hot"


def test_temperature_band_mild():
    assert temperature_band(20) == "mild"


def test_describe_weather_code_known():
    label, category = describe_weather_code(0)
    assert label == "Clear sky"
    assert category == "clear"


def test_describe_weather_code_unknown_falls_back():
    label, category = describe_weather_code(999)
    assert label == "Unknown"


def test_recommend_outfit_cold_day():
    result = recommend_outfit(temp_c=2, precipitation_prob=10, wind_kmh=10, weather_code=2)
    assert "sweater" in result["layers"] or "jacket" in result["layers"]
    assert result["band"] == "cold"


def test_recommend_outfit_hot_day_warns_hydration():
    result = recommend_outfit(temp_c=34, precipitation_prob=0, wind_kmh=5, weather_code=0)
    assert result["band"] == "hot"
    assert any("hydrated" in w.lower() for w in result["warnings"])


def test_recommend_outfit_rainy_day_adds_umbrella():
    result = recommend_outfit(temp_c=18, precipitation_prob=80, wind_kmh=10, weather_code=61)
    assert "umbrella" in result["layers"]
    assert any("rain" in w.lower() for w in result["warnings"])


def test_recommend_outfit_windy_adds_windbreaker():
    result = recommend_outfit(temp_c=15, precipitation_prob=5, wind_kmh=40, weather_code=1)
    assert "windbreaker" in result["layers"]


def test_recommend_outfit_storm_warns():
    result = recommend_outfit(temp_c=22, precipitation_prob=70, wind_kmh=20, weather_code=95)
    assert any("thunderstorm" in w.lower() for w in result["warnings"])
