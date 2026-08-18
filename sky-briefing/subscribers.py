"""
Tiny subscriber list, stored as JSON - no database needed for a project
this size. Each subscriber has their own city, which is exactly what makes
the daily emails personalized instead of one blast to everyone.
"""

import json
import os

SUBSCRIBERS_FILE = os.path.join(os.path.dirname(__file__), "subscribers.json")


def _load():
    if not os.path.exists(SUBSCRIBERS_FILE):
        return []
    with open(SUBSCRIBERS_FILE, "r") as f:
        return json.load(f)


def _save(data):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_subscriber(email, city):
    data = _load()
    # Replace an existing subscription for the same email rather than
    # duplicating it (e.g. they moved cities and re-subscribed)
    data = [s for s in data if s["email"].lower() != email.lower()]
    data.append({"email": email, "city": city})
    _save(data)


def remove_subscriber(email):
    data = _load()
    new_data = [s for s in data if s["email"].lower() != email.lower()]
    removed = len(new_data) != len(data)
    _save(new_data)
    return removed


def all_subscribers():
    return _load()
