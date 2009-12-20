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

def add(apikey, priority=constants.NORMAL, application='txprowl', event='test', description='veryboring'):
    """Add a notification for a particular user.

    @type apikey: L{str}
    @param apikey: api key of the user the message is for (40 bytes long)
    @type priority: one of L{txprowl.constants}
    @param priority: priority of the message.  users may allow EMERGENCY priority notifications while blocking others
    @type application: L{unicode}
    @param application: name you would like your application to be know by (may be up to 256 characters long).
    @type event: L{unicode}
    @param event: name or subject of the event - e.g. for an IM message notification, it might be sender's nickname (may be up to 1024 characters long).
    @type description: L{unicode}
    @param description: body of the notification - e.g. for an IM message notification, it might be the (beginning of) the received message (may be up to 10000 characters long).
    """
    return make_request("add", {
            'apikey': apikey,
            'priority': priority.encode('utf-8'),
            'application': application.encode('utf-8'),
            'event': event.encode('utf-8'),
            'description': description.encode('utf-8')
            })

def verify_api_key(apikey):
    """Verify a given API key is valid.
    Note: This does, by itself, cost an API call.

    @type apikey: L{str}
    @param apikey: api key of the user the message is for (40 bytes long)
    """
    command = "verify"
    data = {'apikey': apikey.encode('utf-8')}
    return do_get_request(
        API_ROOT + command,
        data
        )
