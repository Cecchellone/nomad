import datetime
import win32api
import pytz
import sqlite3
import subprocess
import re
import logging

_DB_PATH = "src/tz_mapping.sqlite3"

class win_time:
    __connection: sqlite3.Connection

    class shift:
        __name: str
        __start: datetime.date
        __bias: datetime.timedelta

        def __init__(
            self,
            name: str = "",
            start: datetime.date = None,
            bias: datetime.timedelta = None,
        ) -> None:
            self.__name = name
            self.__bias = bias
            self.__start = start

        @property
        def start(self) -> tuple:
            if not self.__start:
                return tuple()
            return win_time.__timetuple(self.__start.replace(year=0))

        @property
        def name(self) -> str:
            return self.__name[:32]

        @property
        def bias(self) -> int:
            if not self.__bias:
                return 0
            return self.__bias.total_seconds() // 60

    def __init__(self):
        self.__connection = sqlite3.connect(_DB_PATH)
        self.__connection.create_function("REGEXP", 2, win_time.__regexp)

    @staticmethod
    def __regexp(expr, item):
        reg = re.compile(expr)
        return reg.search(item) is not None

    @staticmethod
    def __timetuple(time: datetime.datetime | datetime.date) -> tuple:
        has_time = isinstance(time, datetime.datetime)

        return (
            time.year,
            time.month,
            time.isocalendar()[2],
            time.day,
            time.hour if has_time else 0,
            time.minute if has_time else 0,
            time.second if has_time else 0,
            (time.microsecond // 1000) if has_time else 0,
        )

    @staticmethod
    def __timezonetuple(
        bias: datetime.timedelta, standard: shift, daylight: shift
    ) -> tuple:
        return (
            bias.total_seconds() // 60,
            standard.name,
            standard.start,
            standard.bias,
            daylight.name,
            daylight.start,
            daylight.bias,
        )

    def set_time(self, time: datetime.datetime) -> None:
        logging.info(f'Setting time to "{time}"')

        win32api.SetSystemTime(win_time.__timetuple(time))

    def set_timezone(self, timezone: pytz.tzinfo) -> None:
        cur = self.__connection.cursor()
        cur.execute(
            "SELECT DISTINCT windows FROM map WHERE linux REGEXP ?;",
            (rf"{timezone.zone}(?:\s|$)",),
        )
        win_tz = cur.fetchone()[0]

        logging.info(f'Setting timezone to "{win_tz}" ("{timezone.zone}")')

        cmd = f"powershell Set-TimeZone -Id '{win_tz}'"
        subprocess.call(cmd, shell=True)
