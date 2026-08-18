"""
Tests for email_content.py. No network calls, no real sending - just checks
that the generated subject/HTML/plain text reflect that specific city and
conditions (the personalization the feature is meant to guarantee).

Run with: pytest test_email_content.py -v
"""

from email_content import build_subject, build_plain_text, build_html, build_email
from outfit_core import recommend_outfit


def sample_outfit(temp=15, rain=10, wind=10, code=2):
    return recommend_outfit(temp_c=temp, precipitation_prob=rain, wind_kmh=wind, weather_code=code)


def sample_current():
    return {"temp": 15, "condition": "Partly cloudy", "wind": 10, "rain_chance": 10}


def sample_forecast():
    return [
        {"date": "2026-08-19", "high": 18, "low": 10, "rain_chance": 20, "condition": "Clear sky"},
        {"date": "2026-08-20", "high": 19, "low": 11, "rain_chance": 15, "condition": "Partly cloudy"},
    ]


def test_subject_includes_city():
    subject = build_subject("Lahore", sample_outfit())
    assert "Lahore" in subject


def test_two_different_cities_get_different_subjects():
    hot = build_subject("Karachi", sample_outfit(temp=38, rain=0))
    cold = build_subject("Murree", sample_outfit(temp=-2, rain=0))
    assert hot != cold


def test_plain_text_contains_city_and_temp():
    text = build_plain_text("Islamabad", sample_current(), sample_outfit(), sample_forecast())
    assert "Islamabad" in text
    assert "15" in text


def test_html_contains_city_and_is_valid_looking():
    html = build_html("Islamabad", sample_current(), sample_outfit(), sample_forecast())
    assert "Islamabad" in html
    assert "<html>" in html
    assert "Unsubscribe" in html


def test_html_includes_unsubscribe_link_with_url():
    html = build_html("Multan", sample_current(), sample_outfit(), sample_forecast(),
                       unsubscribe_url="http://example.com/unsubscribe?email=test@test.com")
    assert "http://example.com/unsubscribe?email=test@test.com" in html


def test_build_email_returns_three_parts():
    subject, html_body, plain_body = build_email(
        "Faisalabad", sample_current(), sample_outfit(), sample_forecast()
    )
    assert subject and html_body and plain_body
    assert "Faisalabad" in subject
    assert "Faisalabad" in html_body
    assert "Faisalabad" in plain_body


def test_warnings_appear_in_all_formats_when_present():
    outfit = sample_outfit(temp=36, rain=0)  # hot -> hydration warning
    subject, html_body, plain_body = build_email("Sukkur", sample_current(), outfit, sample_forecast())
    assert any("hydrat" in w.lower() for w in outfit["warnings"])
    assert "hydrat" in html_body.lower()
    assert "hydrat" in plain_body.lower()
