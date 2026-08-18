"""
Sends today's Sky Briefing to every subscriber - each one gets an email
built fresh from THEIR OWN city's current weather, not a shared broadcast.

Run manually:
    python send_daily_alerts.py

Or schedule it (once a day) with:
- Windows: Task Scheduler, action = run this script
- Mac/Linux: a cron job, e.g.  0 7 * * *  python send_daily_alerts.py
"""

import time

import subscribers
from weather_service import get_conditions_for_city
from email_content import build_email
from email_sender import send_email

UNSUBSCRIBE_BASE_URL = "http://127.0.0.1:5000/unsubscribe"


def run():
    subs = subscribers.all_subscribers()
    if not subs:
        print("No subscribers yet.")
        return

    print(f"Sending alerts to {len(subs)} subscriber(s)...")

    for sub in subs:
        email = sub["email"]
        city = sub["city"]

        data = get_conditions_for_city(city)
        if data is None:
            print(f"  Skipping {email} - couldn't fetch weather for '{city}'")
            continue

        unsubscribe_url = f"{UNSUBSCRIBE_BASE_URL}?email={email}"
        subject, html_body, plain_body = build_email(
            data["city"], data["current"], data["outfit"], data["forecast"],
            unsubscribe_url=unsubscribe_url,
        )

        try:
            send_email(email, subject, html_body, plain_body)
            print(f"  Sent to {email} ({data['city']})")
        except Exception as e:
            print(f"  Failed to send to {email}: {e}")

        # Small delay between sends - sending a burst of identical-looking
        # emails all at once is itself a spam signal to some providers.
        time.sleep(1)


if __name__ == "__main__":
    run()
