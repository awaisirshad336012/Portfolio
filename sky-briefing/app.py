"""
Sky Briefing - a weather-based outfit recommender, plus optional daily
email alerts.

Looks up a city, pulls current + 5-day weather from Open-Meteo (free, no API
key required), and turns it into a plain-language outfit recommendation.
Weather-fetching lives in weather_service.py, recommendation logic in
outfit_core.py, and email building/sending in email_content.py /
email_sender.py - this file only wires them together as web routes.
"""

from flask import Flask, render_template, jsonify, request

from weather_service import get_conditions_for_city
import subscribers

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/weather")
def api_weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "Please enter a city name."}), 400

    data = get_conditions_for_city(city)
    if data is None:
        return jsonify({"error": f"Couldn't find '{city}'. Check the spelling and try again."}), 404

    return jsonify(data)


@app.route("/api/subscribe", methods=["POST"])
def api_subscribe():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email", "").strip()
    city = payload.get("city", "").strip()

    if not email or "@" not in email:
        return jsonify({"error": "Enter a valid email address."}), 400
    if not city:
        return jsonify({"error": "Enter a city."}), 400

    # Confirm the city is real before saving the subscription
    data = get_conditions_for_city(city)
    if data is None:
        return jsonify({"error": f"Couldn't find '{city}'. Check the spelling and try again."}), 404

    subscribers.add_subscriber(email, data["city"])
    return jsonify({"message": f"Subscribed! You'll get daily alerts for {data['city']}."})


@app.route("/api/unsubscribe", methods=["POST"])
def api_unsubscribe():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email", "").strip()
    if not email:
        return jsonify({"error": "Enter your email address."}), 400

    removed = subscribers.remove_subscriber(email)
    if removed:
        return jsonify({"message": "You've been unsubscribed."})
    return jsonify({"error": "That email isn't on the list."}), 404


@app.route("/unsubscribe")
def unsubscribe_page():
    """Simple link target for the unsubscribe link inside emails."""
    email = request.args.get("email", "")
    if email:
        subscribers.remove_subscriber(email)
        return "You've been unsubscribed from Sky Briefing alerts."
    return "Missing email address."


if __name__ == "__main__":
    app.run(debug=True)
