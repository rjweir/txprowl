import sys

from twisted.internet import reactor

from txprowl.core import add, ProwlException, verify_api_key
from txprowl.constants import levels
from txprowl.util import output_result

def notify(*args):
    """dodgy wrapper to look up priority."""
    args = list(args)
    args[1] = levels[args[1]]
    return add(*args)

map = {
    'verify': (verify_api_key, 1, "usage: prowl verify APIKEY"),
    'notify': (notify, 5, "usage: prowl add APIKEY PRIORITY APPLICATION EVENT DESCRIPTION"),
    }

def cmdlinetool(args):
    try:
        command = map[args[0]]
        if len(sys.argv[2:]) != command[1]:
            print command[2], len(sys.argv[2:])
            sys.exit(1)
    except KeyError:
        print "Unknown command"
    else:
        apikey = args[1]
        d = command[0](*args[1:])
        d.addCallback(output_result)
        d.addCallback(done)
        d.addErrback(dump)
        reactor.run()

def dump(data):
    data.trap(ProwlException)
    print str(data.value)
    reactor.stop()

def done(result):
    reactor.stop()
