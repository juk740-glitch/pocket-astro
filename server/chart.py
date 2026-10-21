"""Calculate a natal chart with Swiss Ephemeris.

Usage:
    python chart.py --date 1990-01-01 --time 08:30 --tz America/Chicago \
        --lat 41.88 --lon -87.63
    python chart.py --file ../data/private/me.json [--json]

Longitudes east are positive, west negative. Tropical zodiac, Placidus houses.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import swisseph as swe

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

PLANETS = [
    ("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
    ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
    ("Saturn", swe.SATURN), ("Uranus", swe.URANUS), ("Neptune", swe.NEPTUNE),
    ("Pluto", swe.PLUTO), ("North Node", swe.TRUE_NODE),
]

# Moshier's built-in ephemeris needs no data files and is accurate to well
# under an arcminute for these dates, which is plenty for a chart.
FLAGS = swe.FLG_MOSEPH | swe.FLG_SPEED


def split_longitude(lon):
    """Turn 0-360 ecliptic longitude into sign, degree, minute, second."""
    sign = int(lon // 30)
    within = lon - sign * 30
    deg = int(within)
    minutes = int((within - deg) * 60)
    seconds = int(round(((within - deg) * 60 - minutes) * 60))
    if seconds == 60:
        seconds, minutes = 0, minutes + 1
    if minutes == 60:
        minutes, deg = 0, deg + 1
    return {"sign": SIGNS[sign], "deg": deg, "min": minutes, "sec": seconds,
            "lon": round(lon, 4)}


def house_of(lon, cusps):
    """Which of the 12 houses a longitude falls in, given the cusps."""
    for i in range(12):
        start, end = cusps[i], cusps[(i + 1) % 12]
        span = (end - start) % 360
        if (lon - start) % 360 < span:
            return i + 1
    return 12


def calculate(date, time, tz, lat, lon):
    local = datetime.fromisoformat(f"{date}T{time}").replace(tzinfo=ZoneInfo(tz))
    utc = local.astimezone(timezone.utc)
    jd = swe.julday(utc.year, utc.month, utc.day,
                    utc.hour + utc.minute / 60 + utc.second / 3600)

    cusps, ascmc = swe.houses_ex(jd, lat, lon, b"P")
    cusps = list(cusps[:12])

    planets = []
    for name, body in PLANETS:
        pos, _ = swe.calc_ut(jd, body, FLAGS)
        entry = {"name": name, **split_longitude(pos[0]),
                 "house": house_of(pos[0], cusps),
                 "retrograde": pos[3] < 0}
        planets.append(entry)

    return {
        "utc": utc.isoformat(),
        "utc_offset": local.strftime("%z"),
        "planets": planets,
        "ascendant": split_longitude(ascmc[0]),
        "midheaven": split_longitude(ascmc[1]),
        "houses": [split_longitude(c) for c in cusps],
    }


def fmt(p):
    return f"{p['deg']:2d}°{p['min']:02d}'{p['sec']:02d}\" {p['sign']}"


def print_chart(chart):
    print(f"UTC {chart['utc']}  (offset {chart['utc_offset']})\n")
    for p in chart["planets"]:
        rx = " R" if p["retrograde"] else ""
        print(f"{p['name']:<11} {fmt(p):<22} house {p['house']:>2}{rx}")
    print(f"\n{'Ascendant':<11} {fmt(chart['ascendant'])}")
    print(f"{'Midheaven':<11} {fmt(chart['midheaven'])}\n")
    for i, c in enumerate(chart["houses"], 1):
        print(f"House {i:<5} {fmt(c)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", help="JSON file with date, time, tz, lat, lon")
    ap.add_argument("--date", help="YYYY-MM-DD")
    ap.add_argument("--time", help="HH:MM, local time at the birthplace")
    ap.add_argument("--tz", help="time zone name, e.g. America/New_York")
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lon", type=float)
    ap.add_argument("--json", action="store_true", help="print JSON")
    args = ap.parse_args()

    if args.file:
        with open(args.file) as f:
            birth = json.load(f)
    else:
        birth = {k: getattr(args, k) for k in ("date", "time", "tz", "lat", "lon")}
    missing = [k for k in ("date", "time", "tz", "lat", "lon") if birth.get(k) is None]
    if missing:
        sys.exit(f"missing: {', '.join(missing)}")

    chart = calculate(birth["date"], birth["time"], birth["tz"],
                      birth["lat"], birth["lon"])
    if args.json:
        print(json.dumps(chart, indent=2))
    else:
        print_chart(chart)


if __name__ == "__main__":
    main()
