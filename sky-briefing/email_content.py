"""
Builds the actual email content for a weather alert - subject line, HTML
body, and a plain-text fallback. No sending logic here (see email_sender.py)
and no Flask - just string building, so it's easy to unit test.

Each email is built fresh from that ONE recipient's city and conditions.
There is no shared/broadcast template with blanks filled in - if two
subscribers are in different cities (or the weather changes between sends),
their emails will genuinely say different things. That matters both for
being useful and for not looking like a mass blast to spam filters.
"""

from datetime import datetime


def build_subject(city, outfit):
    """A specific, human subject line - not a generic 'ALERT' blast."""
    band = outfit["band"]
    if outfit["warnings"]:
        return f"{city}: {outfit['warnings'][0]}"
    return f"{city} today: {band} and {outfit['category']}"


def build_plain_text(city, current, outfit, forecast):
    """Plain-text version. Required alongside HTML - mail providers trust
    messages more when a real plain-text alternative is included, and it's
    what shows up in preview panes."""
    lines = [
        f"Sky Briefing for {city}",
        f"{datetime.now().strftime('%A, %d %B %Y')}",
        "",
        f"Right now: {current['temp']}°C, {current['condition']}",
        f"Wind: {current['wind']} km/h  |  Rain chance: {current['rain_chance']}%",
        "",
        outfit["verdict"] + ".",
        "",
        "Wear: " + ", ".join(outfit["layers"]),
    ]
    if outfit["warnings"]:
        lines.append("")
        lines.append("Heads up:")
        for w in outfit["warnings"]:
            lines.append(f"- {w}")

    lines.append("")
    lines.append("Next few days:")
    for day in forecast:
        lines.append(f"  {day['date']}: {day['low']}-{day['high']}°C, {day['condition']}")

    lines.append("")
    lines.append("You're getting this because you subscribed to Sky Briefing alerts for "
                  f"{city}. Unsubscribe any time - see the link in the HTML version of this email.")
    return "\n".join(lines)


def build_html(city, current, outfit, forecast, unsubscribe_url="#"):
    """
    HTML version. Deliberately uses inline styles and simple table layout
    instead of the site's normal CSS - most email clients (Gmail, Outlook)
    strip <style> blocks and modern CSS, so inline styles are what actually
    render reliably across inboxes.
    """
    warnings_html = ""
    if outfit["warnings"]:
        items = "".join(
            f'<li style="margin-bottom:4px;">{w}</li>' for w in outfit["warnings"]
        )
        warnings_html = f"""
        <tr>
          <td style="padding:0 32px 20px;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#3A2A26; border-radius:8px;">
              <tr><td style="padding:14px 18px; color:#E8A08F; font-family:Arial,sans-serif; font-size:13px;">
                <strong style="color:#F2A78F;">Heads up</strong>
                <ul style="margin:8px 0 0; padding-left:18px;">{items}</ul>
              </td></tr>
            </table>
          </td>
        </tr>"""

    layers_html = "".join(
        f'<span style="display:inline-block; background:rgba(127,191,160,0.15); color:#7FBFA0; '
        f'border:1px solid rgba(127,191,160,0.4); border-radius:999px; padding:5px 12px; '
        f'font-size:12px; margin:0 6px 6px 0; font-family:Arial,sans-serif;">{item}</span>'
        for item in outfit["layers"]
    )

    forecast_rows = ""
    for day in forecast:
        forecast_rows += f"""
        <td style="text-align:center; padding:10px 6px; background:#1C2743; border-radius:8px;">
          <div style="color:#8C97B8; font-size:10px; font-family:Arial,sans-serif; text-transform:uppercase; letter-spacing:0.06em;">{day['date'][5:]}</div>
          <div style="color:#F2EFE6; font-size:15px; font-family:Arial,sans-serif; font-weight:bold; margin-top:4px;">{day['high']}°</div>
          <div style="color:#8C97B8; font-size:12px; font-family:Arial,sans-serif;">{day['low']}°</div>
        </td>"""

    return f"""\
<!DOCTYPE html>
<html>
<body style="margin:0; padding:0; background:#0E1424;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#0E1424; padding:32px 0;">
  <tr>
    <td align="center">
      <table width="560" cellpadding="0" cellspacing="0" style="background:#141B2E; border-radius:14px; overflow:hidden;">

        <tr>
          <td style="padding:26px 32px 4px;">
            <div style="color:#8C97B8; font-family:Courier New,monospace; font-size:11px; letter-spacing:0.12em; text-transform:uppercase;">Sky Briefing</div>
            <div style="color:#F2EFE6; font-family:Arial,sans-serif; font-size:24px; font-weight:bold; margin-top:6px;">{city}</div>
            <div style="color:#8C97B8; font-family:Arial,sans-serif; font-size:13px; margin-top:2px;">{datetime.now().strftime('%A, %d %B %Y')}</div>
          </td>
        </tr>

        <tr>
          <td style="padding:20px 32px;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#1C2743; border-radius:10px;">
              <tr>
                <td style="padding:20px;">
                  <span style="color:#E8A33D; font-family:Arial,sans-serif; font-size:34px; font-weight:bold;">{current['temp']}°</span>
                  <span style="color:#8C97B8; font-family:Arial,sans-serif; font-size:14px; margin-left:8px;">{current['condition']}</span>
                  <div style="color:#8C97B8; font-family:Arial,sans-serif; font-size:12px; margin-top:6px;">
                    Wind {current['wind']} km/h &nbsp;·&nbsp; Rain chance {current['rain_chance']}%
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <tr>
          <td style="padding:0 32px 18px;">
            <div style="color:#F2EFE6; font-family:Arial,sans-serif; font-size:17px; line-height:1.5; font-weight:bold;">
              {outfit['verdict']}.
            </div>
          </td>
        </tr>

        <tr>
          <td style="padding:0 32px 20px;">
            {layers_html}
          </td>
        </tr>

        {warnings_html}

        <tr>
          <td style="padding:4px 32px 24px;">
            <div style="color:#8C97B8; font-family:Arial,sans-serif; font-size:11px; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:10px;">Next few days</div>
            <table width="100%" cellpadding="0" cellspacing="4"><tr>{forecast_rows}</tr></table>
          </td>
        </tr>

        <tr>
          <td style="padding:18px 32px; border-top:1px solid #2C3A5E;">
            <div style="color:#5C6B85; font-family:Arial,sans-serif; font-size:11px; line-height:1.6;">
              You're getting this because you subscribed to Sky Briefing alerts for {city}.
              <a href="{unsubscribe_url}" style="color:#7FBFA0;">Unsubscribe</a>
            </div>
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>
</body>
</html>"""


def build_email(city, current, outfit, forecast, unsubscribe_url="#"):
    """Convenience wrapper: returns (subject, html_body, plain_body) together."""
    subject = build_subject(city, outfit)
    html_body = build_html(city, current, outfit, forecast, unsubscribe_url)
    plain_body = build_plain_text(city, current, outfit, forecast)
    return subject, html_body, plain_body
