from urllib import urlencode
from xml.etree import ElementTree
from datetime import datetime

from twisted.web.client import getPage
from twisted.web.error import Error

from txprowl import constants

API_ROOT = "https://prowl.weks.net/publicapi/"

class ProwlException(Exception):
    """Base class to ease catching Prowl-specific errors."""

class AuthError(ProwlException):
    def __str__(self):
        return "Not authorized, the API key given is not valid, and does not correspond to a user."

class MustUseSSL(ProwlException):
    def __str__(self):
        return "Method not allowed, you attempted to use a non-SSL connection to Prowl."

class APILimitError(ProwlException):
    def __str__(self):
        return "Not acceptable, your IP address has exceeded the API limit."

class ProwlServerError(ProwlException):
    def __str__(self):
        return "Internal server error, something failed to execute properly on the Prowl side."
    
error_map = {
    '401': AuthError,
    '405': MustUseSSL,
    '406': APILimitError,
    '500': ProwlServerError,
    }

def fail_handler(failure):
    if failure.check(Error):
        try:
            err_code = failure.value.status
            err = error_map[err_code]
            failure.trap(Error)
            raise err()
        except KeyError:
            pass

def parse_success(response):
    tree = ElementTree.fromstring(response)
    result = tree.find('success')
    ret = int(result.get("remaining")), datetime.fromtimestamp(int(result.get("resetdate")))
    return ret

def do_get_request(url, data):
    d = getPage(
        url + "?" + urlencode(data)
        )
    d.addCallback(parse_success)
    d.addErrback(fail_handler)
    return d

def do_post_request(url, data):
    print "posting %s to %s" % (data, url)
    d = getPage(
        url,
        method='POST',
        postdata=urlencode(data),
        headers={'Content-Type':'application/x-www-form-urlencoded'}
        )
    d.addCallback(parse_success)
    d.addErrback(fail_handler)
    return d

def make_request(command, data):
    return do_post_request(
        API_ROOT + command,
        data
        )

class Add(object):
    """Add a notification for a particular user."""

    def go(self, apikey, priority=constants.NORMAL, application='txprowl', event='test', description='veryboring'):
        return make_request("add", {
                'apikey': apikey,
                'priority': priority,
                'application': application,
                'event': event,
                'description': description
                })

class Verify(object):
    """Verify a given API key is valid."""

    def go(self, apikey):
        command = "verify"
        data = {'apikey': apikey.encode('utf-8')}
        return do_get_request(
            API_ROOT + command,
            data
            )
