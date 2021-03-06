def output_result(args):
    """Nicely format and print the result of a successful API call."""
    remaining, reset_date = args
    print "%d API calls remaining - counter will reset at %s" % (remaining, reset_date.strftime("%H:%M on %Y%m%d"))
    return remaining, reset_date
