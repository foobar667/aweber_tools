#!/usr/bin/env python

from abc import ABCMeta, abstractmethod

from aweber_tools.include.msg import *

from aweber_tools.models.filters.subscribers import \
    FilterAddedBeforeDaysAgo, FilterException, FilterNoOpensSinceDaysAgo

from aweber_tools.models.subscribers import \
    SubscribersAll, SubscriberException, SubscribersException, \
    SubscribersSubscribed

from aweber_tools.utils.export_csv import ExportCsv, ExportCsvException

from future.builtins.misc import input
import os
import sys

TIMEDELTA_30_DAYS_AGO = 30

class ActionException(Exception):
    pass

class Action(object):

    """Action interface."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        """Runs code."""
        pass

    @abstractmethod
    def key(self):
        """Returns the integer key associated with a concrete action."""
        pass

    @abstractmethod
    def name(self):
        """Returns action name."""
        pass

class ActionSubscriberBase(object):

    """Base subscriber-related action class."""

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client):
        self._client = client

    def __init__(self, client=None):
        self._client = client
        self._save_path = None

    def _ask_confirmation(self):

        key = ''
        keys = [INPUT_YES, INPUT_NO]
        i = 0

        while (key not in keys):
            if (i > 0):
                print(SPACE12 + MSG_ACTIONS_AVAILABLE
                      + ', '.join(char for char in keys))
            i += 1
            key = input('\n' + SPACE8 + INPUT_YES_NO).upper()

        if (key == INPUT_YES):
            return True

        return False

    def _create_directory(self, directory):

        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except:
            raise ActionException(ERROR_DIR_CREATE.format(directory))

    def _export_csv(self, subscribers, save_path):

        input('\n' + SPACE8 + MSG_CSV_DOWNLOAD)
        print('\n' + SPACE8 + MSG_EXPORT)

        exporter = ExportCsv()

        try:
            exporter.export(subscribers, save_path)
        except ExportCsvException as e:
            raise ActionException(SPACE12 + ERROR_CAPTION + str(e))

        print(SPACE12 + MSG_DONE)

    def _set_save_path(self):

        tab = SPACE8

        self._save_path = self.client.config.backup_path

        if (not self._save_path):
            tab = SPACE12
            no_path_in_cfg = True
            print('\n' + SPACE8 + MSG_NO_PATH_CSV)
            self._save_path = os.getcwdu()

        try:
            self._create_directory(self._save_path)
        except ActionException as e:
            raise ActionException(SPACE8 + ERROR_CAPTION + str(e))

        try:
            print(tab + MSG_PATH_CSV.format(self._save_path))
        except UnicodeEncodeError:
            path_print = self._save_path.encode('ascii', 'xmlcharrefreplace')
            print(tab + MSG_PATH_CSV.format(path_print))

class DeleteInactive(ActionSubscriberBase):

    """
    Deletes subscribers who haven't opened any emails since 30 days ago and
    subscribed before 30 days ago.
    """

    def execute(self):

        """Implements Action.execute."""

        self._set_save_path()

        subscribers = self._get_subscribers()
        entries_count = len(subscribers)

        if (entries_count <= 0):
            print('\n' + SPACE8 + MSG_SUBSCRIBERS_EMPTY + '\n')
            return

        print ('\n' + SPACE8 + MSG_SUBSCRIBERS_COUNT.format(entries_count))

        if (not self._ask_confirmation()):
            print('')
            return

        self._export_csv(subscribers, self._save_path)

        if (not self._ask_confirmation()):
            print('')
            return

        self._delete_subscribers(subscribers)

    def key(self):

        """Implements Action.key."""

        return 2

    def name(self):

        """Implements Action.name."""

        return ACTION_TITLE_DELETE_INACTIVE

    def _delete_subscribers(self, subscribers):

        print('\n' + SPACE8 + MSG_DELETE)

        deleted_count = 0;
        for subscriber in subscribers:
            try:
                subscriber.delete()
            except SubscriberException:
                raise ActionException(SPACE12 + ERROR_CAPTION + str(e))
            deleted_count += 1

        print(SPACE12 + MSG_DONE + ' ' \
              + MSG_DELETED_ENTRIES.format(deleted_count) + '\n')

    def _get_subscribers(self):

        print('\n' + SPACE8 + MSG_SUBSCRIBERS_GET)

        subscribers = None

        try:
            subscribers = SubscribersSubscribed(self.client).get()
        except SubscribersException as e:
            raise ActionException(SPACE12 + ERROR_CAPTION + str(e))

        try:
            date_filter = FilterAddedBeforeDaysAgo()
            subscribers_filtered_date = \
                date_filter.filter(subscribers, TIMEDELTA_30_DAYS_AGO)

            opens_filter = FilterNoOpensSinceDaysAgo()
            subscribers_filtered_opens = opens_filter.filter(
                subscribers_filtered_date, TIMEDELTA_30_DAYS_AGO)
        except FilterException as e:
            raise ActionException(SPACE12 + ERROR_CAPTION + str(e))

        return subscribers_filtered_opens

class DownloadAll(ActionSubscriberBase):

    """Downloads all subscribers' data as CSV."""

    def execute(self):

        """Implements Action.execute."""

        self._set_save_path()
        subscribers = self._get_subscribers()
        self._export_csv(subscribers, self._save_path)
        print('')

    def key(self):

        """Implements Action.key."""

        return 1

    def name(self):

        """Implements Action.name."""

        return ACTION_TITLE_DOWNLOAD_ALL

    def _get_subscribers(self):

        print('\n' + SPACE8 + MSG_SUBSCRIBERS_GET)

        subscribers = None

        try:
            subscribers = SubscribersAll(self.client).get()
        except SubscribersException as e:
            raise ActionException(SPACE12 + ERROR_CAPTION + str(e))

        return subscribers

class Terminate(object):

    """Terminates the app."""

    def execute(self):

        """Implements Action.execute."""

        print('\n' + MSG_BYE)
        input(INPUT_EXIT)
        sys.exit()

    def key(self):

        """Implements Action.key."""

        return 3

    def name(self):

        """Implements Action.name."""

        return ACTION_TITLE_TERMINATE

Action.register(DownloadAll)
Action.register(DeleteInactive)
Action.register(Terminate)