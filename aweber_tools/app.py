#!/usr/bin/env python

from aweber_api import APIException, AWeberResponse

from aweber_tools.actions import \
    ActionException, DeleteInactive, DownloadAll, Terminate

from aweber_tools.client import \
    Client, ClientAuthException, ClientAuthPageException, ClientException

from aweber_tools.include.logo import APP_LOGO
from aweber_tools.include.msg import *

from future.builtins.misc import input

import getpass
import sys

APP_AUTHORIZE_RETRIES = 2

class AppException(Exception):
    pass

class App(object):

    """
    AWeber tools app controller class.

    Constructor args:
        filename: string; file with configuration params.
    """

    def __init__(self, filename=None):

        self._client = None
        self._filename = filename

        action_delete = DeleteInactive()
        action_download = DownloadAll()
        action_terminate = Terminate()

        self._action_titles = \
            {action_download.key(): action_download.name(),
             action_delete.key(): action_delete.name(),
             action_terminate.key(): action_terminate.name()}

        self._actions = \
            {action_download.key(): action_download,
             action_delete.key(): action_delete,
             action_terminate.key(): action_terminate}

    def run(self):

        """
        Application flow.

        Raises:
            AppException.
        """

        self._print_logo()
        self._set_client()
        self._check_config()

        config = self._client.config
        if (not config.access_token) or (not config.access_secret):
            if (not self._authorize()):
                return
            self._update_config()

        self._connect()
        self._setup_actions()

        while (True):
            try:
                self._select_action()
            except AppException as e:
                print(str(e) + '\n')

    def _authorize(self):

        print('\n' + MSG_AUTH)

        i = 0
        manual_auth = False
        parse_success = False

        # Try to sign in APP_AUTHORIZE_RETRIES+1 times
        while (not parse_success):
            i += 1

            if (i == APP_AUTHORIZE_RETRIES + 2):
                break
            if (i > 1):
                print('\n' + SPACE4 + MSG_AUTH_RETRY + '\n')

            login = input(SPACE4 + INPUT_USERNAME)
            secret = getpass.getpass(SPACE4 + INPUT_PASSWORD)

            # Try to get the verification code
            try:
                parse_success = self._client.authorize_terminal(login, secret)
            except ClientException as e: # Will have to auth manually
                manual_auth = True
                break
            except ClientAuthException as e: # Wrong creds?
                print('\n' + SPACE4 + str(e))
                continue
            except ClientAuthPageException: # Can't parse the response page
                print ('\n' + SPACE4 + MSG_AUTH_PAGE_PARSE)
                manual_auth = True
                break

        browser_success = False
        manual_success = False

        # Will have to to sign-in via the AWeber page
        if (not parse_success) or (manual_auth):

            print('\n' + SPACE4 + MSG_AUTH_MANUAL)
            print(SPACE8 + self._client.auth_url)

            # Open the auth web page
            try:
                browser_success = self._client.authorize_browser()
            except ClientAuthException as e:
                raise AppException(SPACE4 + ERROR_CAPTION + str(e))

            # Ask the user to input the verification code he got from the
            # web page above and try to authorize the app via the API.
            if (browser_success):

                i = 0
                while (not manual_success):
                    i += 1

                    if (i == APP_AUTHORIZE_RETRIES + 2):
                        break
                    if (i > 1):
                        print('\n' + SPACE12 + MSG_AUTH_RETRY + '\n')

                    code = input(SPACE8 + INPUT_CODE)

                    try:
                        manual_success = self._client.verify_code(code)
                    except ClientException as e:
                        print('\n' + SPACE12 + ERROR_CODE)

                    if (manual_success):
                        break

        if (not parse_success) and (not manual_success):
            print('\n' + ERROR_AUTH)
            return False

        return True

    def _check_config(self):

        if (not self._client.config.consumer_key):
            raise AppException(SPACE4 + ERROR_CAPTION + ERROR_NO_CONSUMER_KEY)

        if (not self._client.config.consumer_secret):
            raise AppException(
                SPACE4 + ERROR_CAPTION + ERROR_NO_CONSUMER_SECRET)

    def _connect(self):

        print('\n' + MSG_CONNECTING)

        try:
            self._client.connect()
        except ClientException as e:
            raise AppException(SPACE4 + ERROR_CAPTION + str(e))

        print(SPACE4 + MSG_ACCOUNT_CONNECTED + '\n')

    def _print_logo(self):
        print(APP_LOGO)

    def _select_action(self):

        action_keys = self._action_titles.keys()

        print(ACTION_LIST_HEADER)

        for key in action_keys:
            print(SPACE4 + str(key) + '. ' + self._action_titles[key])

        # Show input prompt until an actual action key is entered

        key = 0
        i = 0
        while (key not in action_keys):
            if (i > 0):
                print(SPACE8 + MSG_ACTIONS_AVAILABLE
                      + ', '.join(str(num) for num in action_keys))
            i += 1
            try:
                key = (int(input('\n' + SPACE4 + INPUT_ACTION)))
            except ValueError:
                pass

        action = self._actions[key]

        try:
            action.execute()
        except ActionException as e:
            raise AppException(str(e))

    def _set_client(self):

        if (self._filename):
            print(MSG_CONFIG_FILE.format(self._filename))

        try:
            self._client = Client(filename=self._filename)
        except ClientException as e:
            raise AppException(SPACE4 + ERROR_CAPTION + str(e))

    def _setup_actions(self):

        action_keys = self._action_titles.keys()
        for key in action_keys:
            self._actions[key].client = self._client

    def _update_config(self):

        try:
            self._client.save_tokens(filename=self._filename)
        except ClientException as e:
            print('\n' + str(e) + ' ' + MSG_CONFIG_KEYS_NOT_SAVED)