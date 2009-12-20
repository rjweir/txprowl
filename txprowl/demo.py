from twisted.internet import reactor

from txprowl.core import Verify, Add, ProwlException

def cmdlinetool(args):
    if args[0] == 'verify':
        print "Verifying..."
        key = args[1]
        output = Verify().go(key)
        output.addCallback(output_info)
        output.addCallback(done)
        output.addErrback(dump)
        reactor.run()
    else:
        print "Unknown command"

def dump(data):
    data.trap(ProwlException)
    print str(data.value)
    reactor.stop()

def output_info(args):
    remaining, reset_date = args
    print "%d API calls remaining - counter will reset at %s" % (remaining, reset_date.strftime("%H:%M on %Y%m%d"))
    return remaining, reset_date
    
def done(result):
    reactor.stop()
