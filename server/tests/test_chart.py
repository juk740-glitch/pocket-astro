"""Tests for chart.py.

Run from the repo root:
    server/.venv/bin/python -m unittest discover -s server/tests -v

The public tests check the calculator against well-documented astronomical
events. The private test compares a real chart against values checked by hand
on astro.com; its data lives in data/private/ and it skips without it.
"""

import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import chart  # noqa: E402

PRIVATE = os.path.join(HERE, "..", "..", "data", "private")


def planet(result, name):
    return next(p for p in result["planets"] if p["name"] == name)


def angle_between(a, b):
    """Smallest difference between two longitudes, in degrees."""
    d = abs(a - b) % 360
    return min(d, 360 - d)


def utc_chart(date, time):
    return chart.calculate(date, time, "UTC", 0.0, 0.0)


class PublicEvents(unittest.TestCase):
    """Times from published almanacs (USNO / timeanddate.com), to the minute."""

    def test_march_equinox_2024_sun_at_0_aries(self):
        sun = planet(utc_chart("2024-03-20", "03:06"), "Sun")
        self.assertLess(angle_between(sun["lon"], 0), 0.02)

    def test_june_solstice_2024_sun_at_0_cancer(self):
        sun = planet(utc_chart("2024-06-20", "20:51"), "Sun")
        self.assertLess(angle_between(sun["lon"], 90), 0.02)

    def test_full_moon_2024_01_25_sun_moon_opposite(self):
        c = utc_chart("2024-01-25", "17:54")
        gap = angle_between(planet(c, "Sun")["lon"], planet(c, "Moon")["lon"])
        self.assertAlmostEqual(gap, 180, delta=0.1)

    def test_eclipse_new_moon_2024_04_08_sun_moon_together(self):
        c = utc_chart("2024-04-08", "18:21")
        gap = angle_between(planet(c, "Sun")["lon"], planet(c, "Moon")["lon"])
        self.assertLess(gap, 0.1)

    def test_mercury_retrograde_april_2024(self):
        self.assertTrue(planet(utc_chart("2024-04-10", "12:00"), "Mercury")["retrograde"])
        self.assertFalse(planet(utc_chart("2024-03-15", "12:00"), "Mercury")["retrograde"])

    def test_sun_and_moon_never_retrograde(self):
        c = utc_chart("2024-04-10", "12:00")
        self.assertFalse(planet(c, "Sun")["retrograde"])
        self.assertFalse(planet(c, "Moon")["retrograde"])

    def test_local_time_uses_historical_offset(self):
        # Noon in New York is 16:00 UTC in July (EDT) and 17:00 in January (EST).
        summer = chart.calculate("2002-07-17", "12:00", "America/New_York", 40.7, -74.0)
        winter = chart.calculate("2002-01-17", "12:00", "America/New_York", 40.7, -74.0)
        self.assertEqual(summer["utc"][11:16], "16:00")
        self.assertEqual(winter["utc"][11:16], "17:00")

    def test_house_of_wraps_past_pisces(self):
        cusps = [350, 20, 50, 80, 110, 140, 170, 200, 230, 260, 290, 320]
        self.assertEqual(chart.house_of(355, cusps), 1)
        self.assertEqual(chart.house_of(5, cusps), 1)
        self.assertEqual(chart.house_of(345, cusps), 12)


@unittest.skipUnless(
    os.path.exists(os.path.join(PRIVATE, "me.json"))
    and os.path.exists(os.path.join(PRIVATE, "me-expected.json")),
    "private birth data not present",
)
class PrivateChart(unittest.TestCase):
    """A real chart, checked by hand against astro.com."""

    TOLERANCE = 1 / 60  # one arcminute

    def setUp(self):
        with open(os.path.join(PRIVATE, "me.json")) as f:
            birth = json.load(f)
        with open(os.path.join(PRIVATE, "me-expected.json")) as f:
            self.expected = json.load(f)
        self.chart = chart.calculate(birth["date"], birth["time"], birth["tz"],
                                     birth["lat"], birth["lon"])

    def test_planets(self):
        for name, want in self.expected["planets"].items():
            got = planet(self.chart, name)
            with self.subTest(planet=name):
                self.assertEqual(got["sign"], want["sign"])
                self.assertLess(angle_between(got["lon"], want["lon"]), self.TOLERANCE)
                self.assertEqual(got["house"], want["house"])
                self.assertEqual(got["retrograde"], want["retrograde"])

    def test_angles(self):
        for key in ("ascendant", "midheaven"):
            with self.subTest(angle=key):
                got, want = self.chart[key], self.expected[key]
                self.assertEqual(got["sign"], want["sign"])
                self.assertLess(angle_between(got["lon"], want["lon"]), self.TOLERANCE)


if __name__ == "__main__":
    unittest.main()
