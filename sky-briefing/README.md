# Sky Briefing

A weather-based outfit recommender. Enter a city, and it pulls live weather
data and tells you what to wear — layers, warnings (rain, wind, storms), and
a 5-day forecast strip — instead of just showing raw numbers. You can also
subscribe to get this as a daily email.

## Why this project

Most beginner weather apps just display temperature. This one adds a small
rule-based recommendation layer on top of live data, uses a real external
API (no key needed), and — as a second feature — sends personalized daily
email alerts built with deliverability in mind rather than a generic mass
email.

## Features

- Look up any city and get current conditions (temperature, wind, rain chance)
- Plain-language outfit recommendation based on temperature, rain, wind, and
  weather type (clear / rain / snow / storm / fog)
- 5-day forecast strip
- Subscribe with an email + city to get a daily briefing email
- No API key required for weather — uses the free Open-Meteo API
- Core logic (recommendations + email content) is fully unit tested

## Project Structure

```
outfit-app/
│
├── app.py                  # Flask app: web routes
├── weather_service.py       # Talks to Open-Meteo (shared by app + alert script)
├── outfit_core.py            # Pure outfit recommendation logic
├── email_content.py           # Builds personalized subject/HTML/plain text
├── email_sender.py             # Sends email via SMTP
├── subscribers.py               # Simple JSON-file subscriber list
├── send_daily_alerts.py          # Script: emails every subscriber their own briefing
├── templates/
│   └── index.html                 # Front-end page
├── test_outfit.py                  # Unit tests for outfit_core.py
├── test_email_content.py            # Unit tests for email_content.py
├── requirements.txt
├── .env.example                      # Template for SMTP credentials
└── .gitignore                         # Keeps .env and subscribers.json out of git
```

Same pattern as before: each concern gets its own file, and the "thinking"
parts (outfit_core.py, email_content.py) have no Flask or SMTP code in them
at all, so they're easy to test in isolation.

## How to Run the Web App

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the app:
   ```
   python app.py
   ```

3. Open your browser:
   ```
   http://127.0.0.1:5000
   ```

## Setting Up Email Alerts

Emails need real SMTP credentials to send - there's nothing to configure
for the weather lookup itself, but alerts won't send without this step.

1. Copy `.env.example` to `.env`.
2. If using Gmail: turn on 2-Step Verification, then generate an
   [App Password](https://myaccount.google.com/apppasswords) and put that
   in `.env` (not your normal Gmail password).
3. Fill in the rest of `.env` with your details.
4. Subscribe to a city from the web app (or add an entry to
   `subscribers.json` directly).
5. Send today's alerts:
   ```
   python send_daily_alerts.py
   ```
6. To send automatically every day, schedule that script with Windows Task
   Scheduler (Windows) or a cron job (Mac/Linux).

### Why emails go to spam, and what this project does about it

- **Only HTML, no plain-text version** looks like a marketing blast to spam
  filters → every email here is sent as multipart (HTML + plain text).
- **Identical content sent to everyone** is a classic spam signal → every
  subscriber's email is built fresh from *their own* city's live weather,
  not one shared template with a name swapped in.
- **Missing unsubscribe link** → every email includes one, and it actually
  works (`/unsubscribe?email=...`).
- **Mismatched or generic sender info** → the From name/address are set
  explicitly and kept consistent, instead of using a random no-reply
  address with a different display name.
- **Hardcoded plaintext passwords in code** → credentials are read from a
  `.env` file (via `python-dotenv`) that's excluded from git, using an app
  password rather than a real account password.

None of this can *guarantee* inbox placement (that also depends on sending
volume, domain reputation, and the recipient's own spam filter), but it
removes the avoidable red flags.

## Running Tests

```
pytest test_outfit.py test_email_content.py -v
```

## Data Source

Weather and geocoding data from [Open-Meteo](https://open-meteo.com/) — a
free weather API that doesn't require signing up for a key.
