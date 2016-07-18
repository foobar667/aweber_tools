#!/usr/bin/env python

from future import standard_library

from aweber_tools.utils.py_compat import PY_VER_MAJOR

import csv
from datetime import datetime

if PY_VER_MAJOR < 3:
    from io import open

import os

COLS_SUBSCRIBER = [
    'Email',
    'Name',
    'Message Number',
    'Date Added',
    'Last Followup Date',
    'Stop Time',
    'Stop Status',
    'Misc',
    'Ad Tracking',
    'IP Address',
    'Web Form URL',
    'Country',
    'Region',
    'City',
    'Postal Code',
    'Latitude',
    'Longitude',
    'DMA Code',
    'Area Code'
]

CSV_DELIMITER = ','
DATE_FORMAT = '%Y-%m-%d_%H.%M.%S'
FILE_EXTENSION = '.csv'

class ExportCsvException(Exception):
    pass

class ExportCsv(object):

    """Exports subscriber data as CSV."""

    def export(self, subscribers, save_path):

        """
            Saves a list of API's 'Subscriber' entries to a CSV file.

            Args:
                subscribers: list of models.subscribers.Subscriber instances;
                save_path: store the generated file here.

            Raises:
                ExportCsvException.
        """

        filename = os.path.join(
            save_path, datetime.now().strftime(DATE_FORMAT) + FILE_EXTENSION)

        try:
            with open(filename, 'wb') as csvfile:
                out = csv.writer(csvfile, delimiter=CSV_DELIMITER,
                                 quoting=csv.QUOTE_ALL)
                out.writerow(COLS_SUBSCRIBER)
                for subscriber in subscribers:
                    entry = self._render_subscriber(subscriber)
                    out.writerow(entry)
        except Exception as e:
            raise ExportCsvException(str(e))

    def _render_subscriber(self, subscriber):

        return [
            subscriber.email,
            subscriber.name,
            subscriber.last_followup_message_number_sent, # Message Number
            subscriber.subscribed_at,
            subscriber.last_followup_sent_at,
            subscriber.unsubscribed_at, # Stop Time
            subscriber.status,
            subscriber.misc_notes,
            subscriber.ad_tracking,
            subscriber.ip_address,
            subscriber.subscription_url, # Web Form URL
            subscriber.country,
            subscriber.region,
            subscriber.city,
            subscriber.postal_code,
            subscriber.latitude,
            subscriber.longitude,
            subscriber.dma_code,
            subscriber.area_code
        ]