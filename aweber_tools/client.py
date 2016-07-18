#!/usr/bin/env python

from aweber_api import AWeberAPI, APIException

from aweber_tools.include.msg import ERROR_NO_AUTH_URL, EXCEPTION_API

from aweber_tools.utils.auth_verifier import \
    AuthErrorException, AuthException, AuthPageException, AuthVerifier

from aweber_tools.utils.config import Config, ConfigException
from aweber_tools.utils.datetime_utils import TimedeltaUtilities

from datetime import datetime, timedelta

import os
import time
import webbrowser

class ClientAuthException(Exception):
    pass

class ClientAuthPageException(Exception):
    pass

class ClientException(Exception):
    pass

class ClientData(object):

    @property
    def auth_url(self):
        return self._api.authorize_url.replace('https://', '')

    @property
    def config(self):
        return self._config

class Client(ClientData):

    """
    AWeber API wrapper.

    Constructor args:
        aweber_tools.utils.config.Config constructor arguments.

    Constructor raises:
        ClientException.
    """

    def __init__(
            self, access_token=None, access_secret=None, consumer_key=None,
            consumer_secret=None, backup_path=None, filename=None):

        self._account = None
        self._api = None
        self._last_request_time = datetime.now() - timedelta(seconds=1)
        self._timedelta_utils = TimedeltaUtilities()

        self._request_token = None
        self._token_secret = None

        try:
            self._config = Config(access_token, access_secret, consumer_key,
                                  consumer_secret, backup_path, filename)
        except ConfigException as e:
            raise ClientException(str(e))

    def authorize_browser(self):

        """
        Try to open the API authorization page in a browser window.

        Returns:
            True is successful.

        Raises:
            ClientException.
        """

        try:
            if (not self._api):
                self._api = AWeberAPI(
                    self.config.consumer_key, self.config.consumer_secret)
                self._request_wait()
                (self._request_token, self._token_secret) = \
                    self._api.get_request_token('oob')
        except APIException as e:
            (excType, excMsg) = str(e).split(': ', 1)
            raise ClientException(
                EXCEPTION_API + ': [' + excType + '] ' + excMsg)

        if (not self._api.authorize_url):
            raise ClientError(ERROR_NO_AUTH_URL)

        # Suppress browser terminal output
        stderr = os.dup(1)
        stdout = os.dup(2)
        os.close(1)
        os.close(2)
        os.open(os.devnull, os.O_RDWR)

        try:
            webbrowser.get().open(self._api.authorize_url)
        except:
            pass
        finally:
            os.dup2(stderr, 1)
            os.dup2(stdout, 2)

        self._api.user.request_token = self._request_token
        self._api.user.token_secret = self._token_secret

        return True

    def authorize_terminal(self, login, secret):

        """
        Tries to send a request the API authorization url and parse the
        verification code from its response.

        Args:
            login: AWeber account username;
            secret: AWeber account password.

        Returns:
            True is successful.

        Raises:
            ClientException;
            ClientAuthException;
            ClientAuthPageException.
        """

        try:
            self._api = AWeberAPI(
                self.config.consumer_key, self.config.consumer_secret)

            self._request_wait()
            request_token, token_secret = self._api.get_request_token('oob')
            self._request_token = request_token
            self._token_secret = token_secret
        except APIException as e:
            (excType, excMsg) = str(e).split(': ', 1)
            raise ClientException(
                EXCEPTION_API + ': [' + excType + '] ' + excMsg)

        if (not self._api.authorize_url):
            raise ClientError(ERROR_NO_AUTH_URL)

        verifier = AuthVerifier()

        try:
            code = verifier.get_code(self._api.authorize_url, login, secret)
        except AuthException as e: # General errors
            raise ClientException(str(e))
        except AuthErrorException as e: # Error text in server's response
            raise ClientAuthException(str(e))
        except AuthPageException: # Request parse errors
            raise ClientAuthPageException

        if (code is None):
            return False

        self._api.user.request_token = request_token
        self._api.user.token_secret = token_secret
        self._api.user.verifier = code

        self._request_wait()

        try:
            access_token, access_secret = self._api.get_access_token()
        except APIException as e:
            (excType, excMsg) = str(e).split(': ', 1)
            raise ClientException(
                EXCEPTION_API + ': [' + excType + '] ' + excMsg)

        self.config.access_token = access_token
        self.config.access_secret = access_secret

        return True

    def connect(self):

        """
        Tries to create a new API instance and access the account
        corresponding with access token and secret.

        Returns:
            True is successful.

        Raises:
            ClientException.
        """

        try:
            if (not self._api):
                self._api = AWeberAPI(
                    self.config.consumer_key, self.config.consumer_secret)

            self._request_wait()
            self._account = self._api.get_account(
                self.config.access_token, self.config.access_secret)
        except APIException as e:
            (excType, excMsg) = str(e).split(': ', 1)
            raise ClientException(
                EXCEPTION_API + ': [' + excType + '] ' + excMsg)

    def delete_subscriber(self, subscriber):

        """
        Executes the 'archive' method of the specified 'Subscriber' entry
        instance of the API.

        Args:
            subscriber: aweber_tools.models.Subscribers.Subscriber,
                        the entry to be deleted.

        Returns:
            True is successful.

        Raises:
            ClientException.
        """

        self._request_wait()

        try:
            subscriber.delete()
        except APIException as e:
            (excType, excMsg) = str(e).split(': ', 1)
            raise ClientException(
                EXCEPTION_API + ': [' + excType + '] ' + excMsg)

    def find_subscribers(self, find_params):

        """
        Executes the 'find subscribers' method of the account instance of the
        API.

        Args:
            find_params: a dictionary of the method's parameters.

        Returns:
            aweber_api.collection.AWeberCollection, a collection of
            aweber.api.entry.AWeberEntry

        Raises:
            ClientException.
        """

        data = None

        self._request_wait()

        try:
            data = self._account.findSubscribers(**find_params)
        except APIException as e:
            (excType, excMsg) = str(e).split(': ', 1)
            raise ClientException(
                EXCEPTION_API + ': [' + excType + '] ' + excMsg)

        return data

    def get_subscriber_activity(self, subscriber):

        """
        Executes the 'getActivity' method of the specified 'Subscriber' entry
        instance of the API.

        Args:
            subscriber: aweber.api.entry.AWeberEntry, Subscriber entry.

        Returns:
            aweber_api.collection.AWeberCollection, a collection
            of subscriber events.

        Raises:
            ClientException.
        """

        data = None

        self._request_wait()

        try:
            data = subscriber.get_activity()
        except APIException as e:
            (excType, excMsg) = str(e).split(': ', 1)
            raise ClientException(
                EXCEPTION_API + ': [' + excType + '] ' +excMsg)

        return data

    def save_tokens(
            self, access_token=None, access_secret=None, filename=None):

        """
        Sets the 'access token' and 'access secret' properties of self.config
        and saves them to disk.

        Args:
            access_token: access token to be saved;
            access_secret: access secret to be saved;
            filename: self.config will save the configuration here.

        Raises:
            ClientException.
        """

        try:
            self.config.save_tokens(access_token, access_secret, filename)
        except ConfigException as e:
            raise ClientException(str(e))

    def verify_code(self, code):

        """
        Sets the verifier code of the API instance ad tries to get access
        token and secret.

        Args:
            code: verifier code.

        Returns:
            True if successful.

        Raises:
            ClientException.
        """

        self._api.user.verifier = code

        self._request_wait()

        try:
            access_token, access_secret = self._api.get_access_token()
        except APIException as e:
            (excType, excMsg) = str(e).split(': ', 1)
            raise ClientException(
                EXCEPTION_API + ': [' + excType + '] ' + excMsg)

        self.config.access_token = access_token
        self.config.access_secret = access_secret

        return True

    def _request_wait(self):

        # The API has a limit of 60 requests/minute per account

        request_time = datetime.now()
        delta = request_time - self._last_request_time
        delta_seconds = self._timedelta_utils.timedelta_total_seconds(delta)

        if (delta_seconds < 1):
            time.sleep(1 - delta_seconds)

        self._last_request_time = datetime.now()