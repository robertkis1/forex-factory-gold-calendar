#!/usr/bin/env python3
"""Maintain a rolling USD high/medium-impact Apple Calendar feed."""
from pathlib import Path
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from urllib.request import Request, urlopen
import argparse
import re

SOURCE = "https://nfs.faireconomy.media/ff_calendar_thisweek.ics"
OUTPUT = Path(__file__).with_name("xauusd_news.ics")


def unfold(raw):
    return re.sub(r"\r?\n[ \t]", "", raw)


def events(raw):
    return re.findall(r"BEGIN:VEVENT\r?\n.*?END:VEVENT", unfold(raw), re.S)


def field(block, name):
    match = re.search(r"^" + re.escape(name) + r"(?:;[^:]*)?:(.*)$", block, re.M)
    return match.group(1).strip() if match else ""


def start_time(block):
    match = re.search(r"^DTSTART(?:;TZID=([^:]+))?:(\d{8}T\d{6}Z?|\d{8})", block, re.M)
    if not match:
        return None
    tz, value = match.groups()
    if value.endswith("Z"):
        return datetime.strptime(value, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    zone = ZoneInfo(tz or "America/New_York")
    if len(value) == 8:
        return datetime.strptime(value, "%Y%m%d").replace(tzinfo=zone)
    return datetime.strptime(value, "%Y%m%dT%H%M%S").replace(tzinfo=zone)


def escape(value):
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace(",", "\\,").replace(";", "\\;")


def selected(block):
    name = field(block, "SUMMARY").lstrip("⁎⁑⁂ ")
    description = field(block, "DESCRIPTION")
    return name.startswith("US ") and ("Impact: High" in description or "Impact: Medium" in description)


def convert(block):
    uid = field(block, "UID")
    start = start_time(block)
    if not uid or start is None:
        return None
    impact = "HIGH" if "Impact: High" in field(block, "DESCRIPTION") else "MEDIUM"
    name = field(block, "SUMMARY").lstrip("⁎⁑⁂ ")
    url = field(block, "URL")
    utc = start.astimezone(timezone.utc)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fmt = lambda dt: dt.strftime("%Y%m%dT%H%M%SZ")
    rendered = "\r\n".join([
        "BEGIN:VEVENT", f"UID:ff-{uid}@xauusd-calendar", f"DTSTAMP:{stamp}",
        f"DTSTART:{fmt(utc)}", f"DTEND:{fmt(utc + timedelta(minutes=5))}",
        f"SUMMARY:{escape(('🔴' if impact == 'HIGH' else '🟠') + ' [' + impact + '] ' + name)}",
        f"DESCRIPTION:{escape('Impact: ' + impact + chr(10) + 'Currency: USD' + chr(10) + 'Source: ' + url + chr(10) + 'Verify times before trading.')}",
        f"URL:{url}", "BEGIN:VALARM", "ACTION:DISPLAY",
        "DESCRIPTION:Forex news in 30 minutes", "TRIGGER:-PT30M",
        "END:VALARM", "END:VEVENT"
    ])
    return uid, utc, rendered


def refresh(raw):
    previous = {}
    if OUTPUT.exists():
        for block in events(OUTPUT.read_text(encoding="utf-8")):
            uid = field(block, "UID").removeprefix("ff-").removesuffix("@xauusd-calendar")
            when = start_time(block)
            if uid and when:
                previous[uid] = (when.astimezone(timezone.utc), block)
    for block in events(raw):
        if selected(block):
            converted = convert(block)
            if converted:
                uid, when, rendered = converted
                previous[uid] = (when, rendered)
    now = datetime.now(timezone.utc)
    kept = sorted(
        ((when, block) for when, block in previous.values()
         if now - timedelta(days=7) <= when <= now + timedelta(days=366)),
        key=lambda item: item[0]
    )
    header = [
        "BEGIN:VCALENDAR", "VERSION:2.0",
        "PRODID:-//XAUUSD Forex Factory Calendar//EN", "CALSCALE:GREGORIAN",
        "X-WR-CALNAME:XAUUSD Forex Factory High + Medium",
        "X-WR-TIMEZONE:Europe/London",
        "REFRESH-INTERVAL;VALUE=DURATION:P1D", "X-PUBLISHED-TTL:PT24H"
    ]
    OUTPUT.write_text("\r\n".join(header + [block for _, block in kept] + ["END:VCALENDAR", ""]), encoding="utf-8")
    print(f"Calendar updated: {len(kept)} events")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path)
    args = parser.parse_args()
    if args.file:
        source = args.file.read_text(encoding="utf-8-sig")
    else:
        request = Request(SOURCE, headers={"User-Agent": "Mozilla/5.0 (compatible; PersonalCalendar/1.0)"})
        with urlopen(request, timeout=25) as response:
            source = response.read().decode("utf-8-sig")
    if "BEGIN:VCALENDAR" not in source:
        raise ValueError("Source was not an ICS calendar")
    refresh(source)
