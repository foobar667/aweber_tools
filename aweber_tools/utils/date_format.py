#!/usr/bin/env python

from aweber_tools.include.msg import ERROR_DATE_STRING

from datetime import datetime, timedelta

FORMAT_DATETIME = '%Y-%m-%d %H:%M:%S'

class DateFormatException(Exception):
    pass

class DateFormat(object):

    """Date formatting utils."""

    def get_date(self, date_string):

        """
        Converts a string to a datetime object.

        Args:
            date_string: a string representation of a date value.

        Returns:
            datetime: the converted result.

        Raises:
            DateFormatException.
        """

        if (date_string is None):
            raise DateFormatException(ERROR_DATE_STRING)

        # Remove ":" character from TimeZone
        formatted_timezone = date_string[:-3] + date_string[-2:]

        # Calculate timeZone Offset In Seconds
        timezone_offset_str = formatted_timezone[-5:]
        timezone_offset = \
            int(timezone_offset_str[-4:-2])*60 + int(timezone_offset_str[-2:])
        timezone_offset *= 60

        if timezone_offset_str[0] == '-':
            timezone_offset = -timezone_offset

        # Format Date to DateTime object with offset
        formatted_date = datetime.strptime(formatted_timezone[:-5],
                                           FORMAT_DATETIME)
        formatted_date += timedelta(seconds=timezone_offset)

        return formatted_date