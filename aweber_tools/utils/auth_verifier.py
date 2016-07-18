#!/usr/bin/env python

from future import standard_library

from aweber_tools.include.msg import ERROR_NO_OAUTH

import urllib
import urllib2
from urlparse import urljoin, urlparse

from HTMLParser import HTMLParser

DIV_ERROR_ID = 'error-header'
OAUTH_TOKEN_PARAM = 'oauth_token'
POST_DISPLAY = 'page'
POST_OAUTH_SUBMIT = 'Allow Access'
REQUEST_HEADERS = {
    'Accept': 'application/xml',
    'Content-Type': 'application/x-www-form-urlencoded'
}

class AuthErrorException(Exception):
    pass

class AuthException(Exception):
    pass

class AuthPageException(Exception):
    pass

class AuthCodeParser(HTMLParser):

    """
    <textarea>PARSE_CONTENT</textarea>
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.data = None
        self.in_code = False
        self.lasttag = None

    def handle_starttag(self, tag, attrs):
        self.in_code = False
        if (tag == 'textarea'):
            self.in_code = True
            self.lasttag = tag

    def handle_endtag(self, tag):
        if (tag == "textarea"):
            self.in_code = False

    def handle_data(self, data):
        if (self.lasttag == 'textarea') and self.in_code and data.strip():
            self.data = data

class AuthErrorParser(HTMLParser):

    """
    <div id="error-header"><span>xxxxx</span>PARSE_CONTENT</div>
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.after_span = False
        self.data = None
        self.in_div = False
        self.lasttag = None

    def handle_starttag(self, tag, attrs):
        if (tag == 'div'):
            for name, value in attrs:
                if (name == 'id') and (value == DIV_ERROR_ID):
                    self.in_div = True
                    self.lasttag = tag

    def handle_endtag(self, tag):
        if (tag == "div") and (self.in_div):
            self.in_div = False
        if (tag == 'span') and (self.in_div):
            self.after_span = True
            self.lasttag = tag

    def handle_data(self, data):
        if (self.lasttag == 'span') and self.in_div and self.after_span \
                and data.strip():
            self.data = data

class AuthVerifier(object):

    """AWeber API authorization page parser."""

    def get_code(self, url, login, secret):

        """
        Sends the POST request to the authorize url and tries to parse
        the verification code from server's response.

        Args:
            url: API application authorization url;
            login: username;
            secret: password;

        Returns:
            String: verification code.

        Raises:
            AuthException;
            AuthErrorException;
            AuthPageException.
        """

        parsed_url = urlparse(url)
        request_url = urljoin(url, parsed_url.path)

        # OAuth token from url's query string params
        oauth_token = self._get_oauth(parsed_url)

        if not oauth_token:
            raise AuthException(ERROR_NO_OAUTH)

        # Send POST data
        try:
            response = self._get_auth_response(request_url, oauth_token,
                                               login, secret)
        except Exception as e:
            raise AuthException(str(e))

        auth_parse_error = False
        auth_error = None

        # Something failed, and the response page contains a div with
        # error info.
        try:
            auth_error = self._get_error_msg(response)
        except:
            auth_parse_error = True

        # The above error means failed authentication.
        if (auth_error):
            raise AuthErrorException(auth_error.strip())

        # No errors - try to get the verification code.
        code_parse_error = False
        try:
            code_value = self._get_code_value(response)
        except :
            code_parse_error = True
            code_value = None

        if (not auth_parse_error) and (not auth_error) and (code_parse_error):
            raise AuthPageException()

        return code_value

    def _get_auth_response(self, url, oauth_token, login, secret):

        post_values = {
            'oauth_username' : login,
            'oauth_password' : secret,
            'oauth_submit' : POST_OAUTH_SUBMIT,
            'oauth_token' : oauth_token,
            'display' : POST_DISPLAY
            }

        post_data = urllib.urlencode(post_values)
        request = urllib2.Request(url, post_data, REQUEST_HEADERS)
        response = urllib2.urlopen(request).read()

        return response

    def _get_code_value(self, response):

        #extraction = Selector(text=response).\
        #    xpath(XPATH_CODE_SELECTOR).extract()

        #return extraction[0]

        parser = AuthCodeParser()
        parser.feed(response)

        return parser.data

    def _get_error_msg(self, response):

        #err = None
        #err = Selector(text=response).css(CSS_ERROR_SELECTOR).extract_first()

        parser = AuthErrorParser()
        parser.feed(response)

        return parser.data

    def _get_oauth(self, url):
        return url.query[len(OAUTH_TOKEN_PARAM + '='):]