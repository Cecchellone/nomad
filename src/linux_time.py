import datetime

def _linux_set_time(time: datetime.datetime):
    import ctypes
    import ctypes.util

    CLOCK_REALTIME = 0

    class timespec(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long), ("tv_nsec", ctypes.c_long)]

    librt = ctypes.CDLL(ctypes.util.find_library("rt"))

    ts = timespec()
    ts.tv_sec = int(time.timestamp())
    ts.tv_nsec = time.microsecond * 1000

    librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))
