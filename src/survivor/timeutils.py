"Time and timezone helpers"

from datetime import datetime, timedelta, tzinfo
import time

def with_local_tz(dt):
    """
    Returns a copy of a datetime with the local timezone attached. No conversion
    happens; `datetime` is assumed to already represent a local time.

    Use this function when interoperating with timezone-aware datetimes (e.g.
    those loaded from the database).
    """
    return dt.replace(tzinfo=LocalTimezone())

def today():
    """
    Returns midnight, today, in the local timezone.
    """
    midnight = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    return with_local_tz(midnight)

def now():
    """
    Returns `datetime.datetime.now()` in the local timezone.
    """
    return with_local_tz(datetime.now())

# Everything below is taken directly from:
# http://docs.python.org/library/datetime.html#tzinfo-objects

ZERO = timedelta(0)
STDOFFSET = timedelta(seconds = -time.timezone)
DSTOFFSET = timedelta(seconds = -time.altzone) if time.daylight else STDOFFSET
DSTDIFF = DSTOFFSET - STDOFFSET

class LocalTimezone(tzinfo):

    def utcoffset(self, dt):
        return DSTOFFSET if self._isdst(dt) else STDOFFSET

    def dst(self, dt):
        return DSTDIFF if self._isdst(dt) else ZERO

    def tzname(self, dt):
        return time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = time.mktime(tt)
        tt = time.localtime(stamp)
        return tt.tm_isdst > 0
