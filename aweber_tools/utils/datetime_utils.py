#!/usr/bin/env python

from datetime import datetime, timedelta

class TimedeltaUtilities(object):

    """DateTime utils."""

    def timedelta_total_seconds(self, timedelta):
        return (
            timedelta.microseconds + 0.0 +
            (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) /10**6