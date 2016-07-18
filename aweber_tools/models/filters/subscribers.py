#!/usr/bin/env python

from abc import ABCMeta, abstractmethod

from aweber_tools.include.msg import ERROR_FILTER_DATA
from aweber_tools.utils.date_format import DateFormat, DateFormatException

from datetime import datetime, timedelta
import time

TIMEDELTA_1_DAY_AGO = 1

class FilterException(Exception):
    pass

class FilterSubscribers(object):

    """Removes subscribers from the list based on filter used."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def filter(self, subscribers, days_ago):
        """Returns a filtered list."""
        pass

class FilterAddedBeforeDaysAgo(object):

    """
    Returns subscribers added before X days ago.

    Implements:
            FilterSubscribers.
    """

    def filter(self, subscribers, days_ago=TIMEDELTA_1_DAY_AGO):

        """
        Iterates over the 'subscribers' list and appends its items to the
        result if their 'subscribed_at' dates are less than
        [now() - 'days_ago' * DAYS].

        Args:
            subscribers: a list of aweber_api.models.subscribers.Subscriber
                         instances;
            days_ago: int, default: TIMEDELTA_1_DAY_AGO.

        Returns:
            a filtered a list of aweber_api.models.subscribers.Subscriber
            instances.

        Implements:
            FilterSubscribers.filter

        Raises:
            FilterException.
        """

        if (subscribers is None):
            raise FilterException(ERROR_FILTER_DATA)

        subscribers_filtered = []
        formatter = DateFormat()

        x_days_ago = datetime.now() - timedelta(days=days_ago)

        try:
            for subscriber in subscribers:
                subscription_date = \
                    formatter.get_date(subscriber.subscribed_at)
                if subscription_date <= x_days_ago:
                    subscribers_filtered.append(subscriber)
        except DateFormatException as e:
            raise FilterException(str(e))

        return subscribers_filtered

class FilterNoOpensSinceDaysAgo(object):

    """
    Returns subscribers with no opens since X days ago.
    
    Implements:
            FilterSubscribers.
    """

    def filter(self, subscribers, days_ago=TIMEDELTA_1_DAY_AGO):

        """
        Iterates over the 'subscribers' list and appends its items to the
        result if their 'get_activity' method's result list doesn't contain
        events with dates after [now() - 'days_ago' * DAYS].

        Args:
            subscribers: a list of aweber_api.models.subscribers.Subscriber
                         instances;
            days_ago: int, default: TIMEDELTA_1_DAY_AGO.

        Returns:
            a filtered a list of aweber_api.models.subscribers.Subscriber
            instances.

        Implements:
            FilterSubscribers.filter

        Raises:
            FilterException.
        """

        if (subscribers is None):
            raise FilterException(ERROR_FILTER_DATA)

        subscribers_filtered = []
        formatter = DateFormat()

        x_days_ago = datetime.now() - timedelta(days=days_ago)

        try:
            for subscriber in subscribers:
                activity = subscriber.get_activity()
                for event in activity:
                    event_date = formatter.get_date(event.event_time)
                    if event_date <= x_days_ago:
                        subscribers_filtered.append(subscriber)
                        break
        except Exception as e:
            raise FilterException(str(e))

        return subscribers_filtered

FilterSubscribers.register(FilterAddedBeforeDaysAgo)
FilterSubscribers.register(FilterNoOpensSinceDaysAgo)