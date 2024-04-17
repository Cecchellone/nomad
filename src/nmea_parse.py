import re
import datetime
import pytz

NMEA_0183_TIME = re.compile(
    r"^\$GPZDA,(?P<time>\d{6}.\d{3}),(?P<day>\d{2}),(?P<month>\d{2}),(?P<year>\d{4}),(?P<tz_h>\d{2}),(?P<tz_m>\d{2})\*(?P<checksum>\d{2})$"
)
NMEA_LATITUDE = re.compile(
    r"^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$"
)
NMEA_LONGITUDE = re.compile(
    r"^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$"
)


def nmea_to_datetime(nmea_time: str) -> datetime.datetime:
    matches = NMEA_0183_TIME.match(nmea_time)
    if not matches:
        raise ValueError("Invalid NMEA time format")
    seconds = float(matches.group("time"))
    microseconds = int((seconds - int(seconds)) * 1000000)
    minutes = int(seconds // 60) % 60
    hours = int(seconds // 3600) % 24
    seconds = int(seconds) % 60
    day = int(matches.group("day"))
    month = int(matches.group("month"))
    year = int(matches.group("year"))

    offset_hours = int(matches.group("tz_h"))
    offset_minutes = int(matches.group("tz_m"))

    timezone = pytz.FixedOffset(offset_hours * 60 + offset_minutes)

    return datetime.datetime(
        year, month, day, hours, minutes, seconds, microseconds, timezone
    )


def nmea_to_coordinates(nmea_position: str) -> tuple[float, float]:
    latitude = NMEA_LATITUDE.match(nmea_position).group(0)
    longitude = NMEA_LONGITUDE.match(nmea_position).group(0)
    return float(latitude), float(longitude)
