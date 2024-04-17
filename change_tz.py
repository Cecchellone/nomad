import sys
import pytz
import argparse
from timezonefinder import TimezoneFinder

from src.windows_time import win_time
from src.nmea_parse import nmea_to_coordinates

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="change_time.py", description="Change system time to the one received from GPS"
    )

    position = parser.add_mutually_exclusive_group(required=True)

    position.add_argument(
        "--nmea",
        type=str,
        help="NMEA position string",
    )

    position.add_argument(
        "--coordinates",
        type=float,
        nargs=2,
        metavar=("LATITUDE", "LONGITUDE"),
        help="Latitude and longitude coordinates in decimal format",
    )

    args = parser.parse_args()

    obj = TimezoneFinder()

    if args.nmea:
        latitude, longitude = nmea_to_coordinates(args.nmea)
    else:
        latitude, longitude = args.coordinates

    tz_name = obj.timezone_at(lat=latitude, lng=longitude)

    tz = pytz.timezone(tz_name)

    if sys.platform == "linux2":
        # _linux_set_time(set_date)
        pass
    elif sys.platform == "win32":
        wt = win_time()
        wt.set_timezone(tz)
