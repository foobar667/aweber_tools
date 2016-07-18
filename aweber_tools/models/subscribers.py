#!/usr/bin/env python

from abc import ABCMeta, abstractmethod

from aweber_tools.client import ClientException
from aweber_tools.include.msg import ERROR_CLIENT

from future.builtins import super

API_SUBSCRIBER_STATUS_PARAM = 'status'
API_SUBSCRIBER_STATUS_VALUE_SUBSCRIBED = 'subscribed'

class SubscriberException(Exception):
    pass

class SubscribersException(Exception):
    pass

class FindParams(object):

    """Passes filters to the subscribers resource find() method of the API."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def params(self):
        """Returns filtering params."""
        pass

class FindAll(object):

    """
    No filtering params.
    
    Implements:
        FindParams.
    """

    def params(self):
        return {}

class FindSubscribed(object):

    """
    Status = subscribed.

    Implements:
        FindParams.
    """

    def params(self):
        return {API_SUBSCRIBER_STATUS_PARAM:
                API_SUBSCRIBER_STATUS_VALUE_SUBSCRIBED}

FindParams.register(FindAll)
FindParams.register(FindSubscribed)

class SubscriberData(object):

    @property
    def ad_tracking(self):
        return self._ad_tracking

    @property
    def area_code(self):
        return self._area_code

    @property
    def city(self):
        return self._city

    @property
    def country(self):
        return self._country

    @property
    def custom_fields(self):
        return self._custom_fields

    @property
    def dma_code(self):
        return self._dma_code

    @property
    def email(self):
        return self._email

    @property
    def id(self):
        return self._id

    @property
    def ip_address(self):
        return self._ip_address

    @property
    def is_verified(self):
        return self._is_verified

    @property
    def last_followup_message_number_sent(self):
        return self._last_followup_message_number_sent

    @property
    def last_followup_sent(self):
        return self._last_followup_sent

    @property
    def last_followup_sent_at(self):
        return self._last_followup_sent_at

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def misc_notes(self):
        return self._misc_notes

    @property
    def name(self):
        return self._name

    @property
    def postal_code(self):
        return self._postal_code

    @property
    def region(self):
        return self._region

    @property
    def status(self):
        return self._status

    @property
    def subscribed_at(self):
        return self._subscribed_at

    @property
    def subscription_method(self):
        return self._subscription_method

    @property
    def subscription_url(self):
        return self._subscription_url

    @property
    def tags(self):
        return self._tags

    @property
    def unsubscribe_method(self):
        return self._unsubscribe_method

    @property
    def unsubscribed_at(self):
        return self._unsubscribed_at

    @property
    def verified_at(self):
        return self._verified_at

class Subscriber(SubscriberData):

    """
    AWeber API Subscriber entry representation.

    Constructor args:
        client: aweber_tools.client.Client;
        data: aweber_api.AWeberEntry, subscriber data.

    Constructor raises:
        ClientException.
    """

    @property
    def client(self):
        return self._client

    def __init__(self, client, data=None):

        if (client is None):
            raise SubscriberException(ERROR_CLIENT)

        self._client = client
        self._data = data

        self._ad_tracking = None
        self._area_code = None
        self._city = None
        self._country = None
        self._custom_fields = None
        self._dma_code = None
        self._email = None
        self._id = None
        self._ip_address = None
        self._is_verified = None
        self._last_followup_message_number_sent = None
        self._last_followup_sent = None
        self._last_followup_sent_at = None
        self._latitude = None
        self._longitude = None
        self._misc_notes = None
        self._name = None
        self._postal_code = None
        self._region = None
        self._status = None
        self._subscribed_at = None
        self._subscription_method = None
        self._subscription_url = None
        self._tags = None
        self._unsubscribe_method = None
        self._unsubscribed_at = None
        self._verified_at = None

        if (self._data is None):
            return

        self._ad_tracking = self._data.ad_tracking
        self._area_code = self._data.area_code
        self._city = self._data.city
        self._country = self._data.country
        self._custom_fields = self._data.custom_fields
        self._dma_code = self._data.dma_code
        self._email = self._data.email
        self._id = self._data.id
        self._ip_address = self._data.ip_address
        self._is_verified = self._data.is_verified
        self._last_followup_message_number_sent = \
            self._data.last_followup_message_number_sent

        if (hasattr(self._data, 'last_followup_sent')):
            self._last_followup_sent = self._data.last_followup_sent

        self._last_followup_sent_at = self._data.last_followup_sent_at
        self._latitude = self._data.latitude
        self._longitude = self._data.longitude
        self._misc_notes = self._data.misc_notes
        self._name = self._data.name
        self._postal_code = self._data.postal_code
        self._region = self._data.region
        self._status = self._data.status
        self._subscribed_at = self._data.subscribed_at
        self._subscription_method = self._data.subscription_method
        self._subscription_url = self._data.subscription_url

        if (hasattr(self._data, 'tags')):
            self._tags = self._data.tags

        self._unsubscribe_method = self._data.unsubscribe_method
        self._unsubscribed_at = self._data.unsubscribed_at
        self._verified_at = self._data.verified_at

    def delete(self):

        """
        Executes the 'delete_subscriber' method of
        aweber_tools.client.Client.

        Raises:
            SubscriberException.
        """

        try:
            self.client.delete_subscriber(self._data)
        except ClientException as e:
            raise SubscriberException(str(e))

    def get_activity(self):

        """
        Executes the 'get_subscriber_activity' method of
        aweber_tools.client.Client.

        Raises:
            SubscriberException.
        """

        data = None

        try:
            data = self.client.get_subscriber_activity(self._data)
        except ClientException as e:
            raise SubscriberException(str(e))

        return data

class SubscribersData(object):

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client):
        self._client = client

    @property
    def subscribers(self):
        return self._subscribers

    @property
    def find_params(self):
        return self._find_params

    @find_params.setter
    def find_params(self, find_params):
        self._find_params = find_params

class Subscribers(SubscribersData):

    """
    A collection of 'Subscriber' instances.

    Constructor args:
        client: aweber_tools.client.Client;
        find_params: instance of a class that implements the 'FindParams'
                     interface, used as a filter for 'get()'.
    """

    def __init__(self, client, find_params=None):

        self._client = client
        self._subscribers = []
        self._find_params = find_params

    def get(self):

        """
        Fetches subscriber data via API.

        Returns:
            a list of 'Subscriber' instances.

        Raises:
            SubscribersException.
        """

        if (self.client is None):
            raise SubscribersException(ERROR_CLIENT)

        find_params = []
        if (self.find_params):
            find_params = self.find_params.params()

        subscribers = []

        try:
            subscribers = self.client.find_subscribers(find_params)
        except ClientException as e:
            raise SubscribersException(str(e))

        try:
            for subscriber in subscribers:
                self.subscribers.append(Subscriber(self._client, subscriber))
        except SubscriberException as e:
            raise SubscribersException(str(e))

        return self.subscribers

class SubscribersAll(Subscribers):

    """All subscribers."""

    def __init__(self, client):
        super().__init__(client, FindAll())

class SubscribersSubscribed(Subscribers):

    """Subscribers with the 'subscribed' status."""

    def __init__(self, client):
        super().__init__(client, FindSubscribed())