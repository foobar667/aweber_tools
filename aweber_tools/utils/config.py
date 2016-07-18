#!/usr/bin/env python


from future import standard_library

from aweber_tools.utils.py_compat import PY_VER_MAJOR

from aweber_tools.include.msg import \
    ERROR_CONFIG_NO_FILE, ERROR_CONFIG_READ, ERROR_CONFIG_TOO_LARGE

import codecs
from configparser import ConfigParser, RawConfigParser

if PY_VER_MAJOR < 3:
    from io import open

import os

MAX_FILE_SIZE = 1048576
SECTION_ACCOUNT = 'account'
SECTION_FILES = 'files'
VALUE_ACCESS_TOKEN = 'access_token'
VALUE_ACCESS_SECRET = 'access_secret'
VALUE_BACKUP_PATH = 'backup_path'
VALUE_CONSUMER_KEY = 'consumer_key'
VALUE_CONSUMER_SECRET = 'consumer_secret'

class ConfigException(Exception):
    pass

class ConfigData(object):

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        self._access_token = access_token

    @property
    def access_secret(self):
        return self._access_secret

    @access_secret.setter
    def access_secret(self, access_secret):
        self._access_secret = access_secret

    @property
    def backup_path(self):
        return self._backup_path

    @backup_path.setter
    def backup_path(self, backup_path):
        self._backup_path = backup_path

    @property
    def consumer_key(self):
        return self._consumer_key

    @consumer_key.setter
    def consumer_key(self, consumer_key):
        self._consumer_key = consumer_key

    @property
    def consumer_secret(self):
        return self._consumer_secret

    @consumer_secret.setter
    def consumer_secret(self, consumer_secret):
        self._consumer_secret = consumer_secret

class Config(ConfigData):

    """
    Application settings.

    Constructor args:
        access_token, access_secret: an AWeber account's keys for access to
            itself via the API;
        consumer_key, consumer_secret: an API application's keys;
        backup_path: an absolute/relative path to store application data;
        filename: load configuration values from this file if specified.
    """

    def __init__(
            self, access_token=None, access_secret=None, consumer_key=None,
            consumer_secret=None, backup_path=None, filename=None):

        if filename is None:
            self._access_token = access_token
            self._access_secret = access_secret
            self._consumer_key = consumer_key
            self._consumer_secret = consumer_secret
            self._backup_path = backup_path
        else:
            self._access_token = None
            self._access_secret = None
            self._consumer_key = None
            self._consumer_secret = None
            self._backup_path = None
            self.load_from_file(filename)

    def load_from_file(self, filename=None):

        """
        Loads config values from 'filename'.

        See the default file for structure.
        Configs larger than MAX_FILE_SIZE are skipped.
        Leading and trailing whitespace is removed.

        Args:
            filename: a UTF-8 config file.

        Raises:
            ConfigException.
        """

        # Skip non-existing and huge files

        if not os.path.isfile(filename):
            raise ConfigException(ERROR_CONFIG_NO_FILE)

        if os.path.getsize(filename) > MAX_FILE_SIZE:
            raise ConfigException(ERROR_CONFIG_TOO_LARGE)

        try:
            with open(filename, encoding='UTF-8') as fp:
                self._parser = UnicodeConfigParser(allow_no_value=True)
                if PY_VER_MAJOR == 3:
                    self._parser = ConfigParser(allow_no_value = True)
                    self._parser.read_file(fp)
                else:
                    self._parser = UnicodeConfigParser(allow_no_value=True)
                    self._parser.readfp(fp)
        except:
            raise ConfigException(ERROR_CONFIG_READ)

        try:
            self.consumer_key = self._parser.get(
                SECTION_ACCOUNT, VALUE_CONSUMER_KEY
            )
        except:
            self.consumer_key = ''
        self.consumer_key = self.consumer_key.strip()

        try:
            self.consumer_secret = self._parser.get(
                SECTION_ACCOUNT, VALUE_CONSUMER_SECRET
            )
        except:
            self.consumer_secret = ''
        self.consumer_secret = self.consumer_secret.strip()

        try:
            self.access_token = self._parser.get(
                SECTION_ACCOUNT, VALUE_ACCESS_TOKEN
            )
        except:
            self.access_token = ''
        self.access_token = self.access_token.strip()

        try:
            self.access_secret = self._parser.get(
                SECTION_ACCOUNT, VALUE_ACCESS_SECRET
            )
        except:
            self.access_secret = ''
        self.access_secret = self.access_secret.strip()

        try:
            self.backup_path = self._parser.get(
                SECTION_FILES, VALUE_BACKUP_PATH
            )
        except:
            self.backup_path = ''
        self.backup_path = self.backup_path.strip()

    def save_tokens(
            self, access_token=None, access_secret=None, filename=None):

        """
        Sets access token and secret and saves it to 'filename' if set.

        Args:
            access_token: access token string;
            access_secret: access secret string;
            filename: a UTF-8 config file.

        Raises:
            ConfigException.
        """

        token = access_token
        secret = access_secret

        if (token is None):
            token = self.access_token
        if (secret is None):
            secret = self.access_secret

        self.access_token = self._parser.set(
            SECTION_ACCOUNT, VALUE_ACCESS_TOKEN, token
        )
        self.access_secret = self._parser.set(
            SECTION_ACCOUNT, VALUE_ACCESS_SECRET, secret
        )

        if (not filename):
            return

        try:
            with codecs.open(filename, 'w', 'UTF-8') as fp:
                self._parser.write(fp)
        except Exception as e:
            raise ConfigException(str(e))

class UnicodeConfigParser(RawConfigParser):
 
    def __init__(self, *args, **kwargs):
        RawConfigParser.__init__(self, *args, **kwargs)
 
    def write(self, fp):
        """Fixed Unicode output."""
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write(
                    "%s = %s\n" % (key, unicode(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key != "__name__":
                    fp.write("%s = %s\n" %
                             (key, unicode(value).replace('\n','\n\t')))
            fp.write("\n")
 
    # This function is needed to override default lower-case conversion
    # of the parameter's names. They will be saved 'as is'.
    def optionxform(self, strOut):
        return strOut