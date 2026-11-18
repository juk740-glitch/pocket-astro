"""Print where the planets are at a given moment.

Usage:
    .venv/bin/python3 positions.py                     # right now
    .venv/bin/python3 positions.py "2026-11-18 14:30"  # a date and time in UTC

For each planet it shows the zodiac sign, the degree within that sign, and
"Rx" if the planet is retrograde (appears to move backwards from Earth).

Uses the tropical zodiac and Swiss Ephemeris's built-in Moshier ephemeris,
which needs no extra data files and is accurate to about a second of arc,
far finer than astrology needs.
"""

import sys
from datetime import datetime, timezone

import swisseph as swe

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

PLANETS = [
    ("Sun", swe.SUN),
    ("Moon", swe.MOON),
    ("Mercury", swe.MERCURY),
    ("Venus", swe.VENUS),
    ("Mars", swe.MARS),
    ("Jupiter", swe.JUPITER),
    ("Saturn", swe.SATURN),
    ("Uranus", swe.URANUS),
    ("Neptune", swe.NEPTUNE),
    ("Pluto", swe.PLUTO),
]

# Built-in ephemeris (no data files) + also compute speed, for retrogrades.
FLAGS = swe.FLG_MOSEPH | swe.FLG_SPEED


def parse_moment(args):
    """Return a UTC datetime from the command line, or now if none given."""
    if not args:
        return datetime.now(timezone.utc)
    try:
        moment = datetime.strptime(args[0], "%Y-%m-%d %H:%M")
    except ValueError:
        sys.exit('Give the date as "YYYY-MM-DD HH:MM" in UTC, for example "2026-11-18 14:30".')
    return moment.replace(tzinfo=timezone.utc)


def planet_positions(moment):
    """Return a list of dicts, one per planet, for a UTC datetime."""
    hours = moment.hour + moment.minute / 60 + moment.second / 3600
    jd = swe.julday(moment.year, moment.month, moment.day, hours)
    results = []
    for name, body in PLANETS:
        values, _ = swe.calc_ut(jd, body, FLAGS)
        longitude, speed = values[0], values[3]
        results.append({
            "name": name,
            "longitude": longitude,             # 0-360 degrees around the zodiac
            "sign": SIGNS[int(longitude // 30)],
            "degree": longitude % 30,           # 0-30 degrees within the sign
            "retrograde": speed < 0,
        })
    return results


def format_degree(degree):
    """26.04 -> 26°02'"""
    whole = int(degree)
    minutes = int(round((degree - whole) * 60))
    if minutes == 60:
        whole, minutes = whole + 1, 0
    return f"{whole:2d}°{minutes:02d}'"


def main():
    moment = parse_moment(sys.argv[1:])
    print(f"Planet positions for {moment:%Y-%m-%d %H:%M} UTC (tropical zodiac)\n")
    for p in planet_positions(moment):
        rx = "  Rx" if p["retrograde"] else ""
        print(f"  {p['name']:<8} {format_degree(p['degree'])} {p['sign']}{rx}")


if __name__ == "__main__":
    main()
