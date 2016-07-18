#!/usr/bin/env python

ACTION_LIST_HEADER = 'Available actions:'
ACTION_TITLE_DELETE_INACTIVE = 'Delete inactive users.'
ACTION_TITLE_DOWNLOAD_ALL = 'Download subscriber database.'
ACTION_TITLE_TERMINATE = 'Exit.'

ERROR_AUTH = "Can't authorize."
ERROR_CAPTION = '!!! Error: '
ERROR_CLIENT = 'no API client specified.'
ERROR_CODE = 'Invalid code.'
ERROR_CONFIG_NO_FILE = "can't open file."
ERROR_CONFIG_READ = "Can't read config data."
ERROR_CONFIG_TOO_LARGE = 'file too large.'
ERROR_DATE_STRING = 'no date specified.'
ERROR_DIR_CREATE = "can't create directory {0}."
ERROR_FILTER_DATA = 'no data to filter specified.'
ERROR_NO_AUTH_URL = 'no authorization URL.'
ERROR_NO_CONSUMER_KEY = 'no consumer key set.'
ERROR_NO_CONSUMER_SECRET = 'no consumer secret set.'
ERROR_NO_OAUTH = 'no OAuth token.'

EXCEPTION_API = 'API Exception'

INPUT_ACTION = 'Type action number: '
INPUT_AUTH_CODE = 'Type code here: '
INPUT_CODE = 'Verification code: '
INPUT_EXIT = 'Press any key to exit...'
INPUT_NO = 'N'
INPUT_PASSWORD = 'Password: '
INPUT_USERNAME = 'Username: '
INPUT_YES = 'Y'
INPUT_YES_NO = 'Y/N to continue: '

MSG_ACCOUNT_CONNECTED = 'Success!'
MSG_ACTIONS_AVAILABLE = 'Available actions: '
MSG_AUTH = 'Access token/secret not set. Authorizing...'
MSG_AUTH_MANUAL = 'Please, authorize via the webpage: https://'
MSG_AUTH_PAGE_PARSE = "Can't parse server response."
MSG_AUTH_RETRY = 'Retrying...'
MSG_BYE = 'Have a nice day!'
MSG_CONFIG_FILE = 'Reading configuration from [{0}]...'
MSG_CONFIG_KEYS_NOT_SAVED = 'New config keys have not been saved!'
MSG_CONNECTING = 'Connecting to AWeber...'
MSG_CSV_DOWNLOAD = 'Press any key to download backup CSV...'
MSG_DELETE = 'Deleting entries...'
MSG_DELETED_ENTRIES = '{0} entries deleted.'
MSG_DONE = 'Done.'
MSG_EXPORT = 'Exporting...'
MSG_NO_PATH_CSV = 'Backup directory not set. Using current working directory.'
MSG_PATH_CSV = 'Using directory {0}.'
MSG_SUBSCRIBERS_COUNT = 'Number of entries to be deleted is {0}.'
MSG_SUBSCRIBERS_EMPTY = 'No entries found.'
MSG_SUBSCRIBERS_GET = 'Retrieving subscribers data...'

SPACE4 = '    '
SPACE8 = '        '
SPACE12 = '            '

__all__ = [
    'ACTION_LIST_HEADER',
    'ACTION_TITLE_DELETE_INACTIVE',
    'ACTION_TITLE_DOWNLOAD_ALL',
    'ACTION_TITLE_TERMINATE',

    'ERROR_AUTH',
    'ERROR_CAPTION',
    'ERROR_CLIENT',
    'ERROR_CODE',
    'ERROR_CONFIG_NO_FILE',
    'ERROR_CONFIG_READ',
    'ERROR_CONFIG_TOO_LARGE',
    'ERROR_DATE_STRING',
    'ERROR_DIR_CREATE',
    'ERROR_FILTER_DATA',
    'ERROR_NO_AUTH_URL',
    'ERROR_NO_CONSUMER_KEY',
    'ERROR_NO_CONSUMER_SECRET',
    'ERROR_NO_OAUTH',

    'EXCEPTION_API',

    'INPUT_ACTION',
    'INPUT_AUTH_CODE',
    'INPUT_CODE',
    'INPUT_EXIT',
    'INPUT_NO',
    'INPUT_PASSWORD',
    'INPUT_USERNAME',
    'INPUT_YES',
    'INPUT_YES_NO',

    'MSG_ACCOUNT_CONNECTED',
    'MSG_ACTIONS_AVAILABLE',
    'MSG_AUTH',
    'MSG_AUTH_MANUAL',
    'MSG_AUTH_PAGE_PARSE',
    'MSG_AUTH_RETRY',
    'MSG_BYE',
    'MSG_CONFIG_FILE',
    'MSG_CONFIG_KEYS_NOT_SAVED',
    'MSG_CONNECTING',
    'MSG_CSV_DOWNLOAD',
    'MSG_DELETE',
    'MSG_DELETED_ENTRIES',
    'MSG_DONE',
    'MSG_EXPORT',
    'MSG_NO_PATH_CSV',
    'MSG_PATH_CSV',
    'MSG_SUBSCRIBERS_COUNT',
    'MSG_SUBSCRIBERS_EMPTY',
    'MSG_SUBSCRIBERS_GET',
    'SPACE4',
    'SPACE8',
    'SPACE12'
]