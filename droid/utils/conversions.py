import datetime


def ms_to_hours(ms):
    """Convert milliseconds to hours"""
    return round(ms / 60.0 / 60.0 / 1000.0, 2)


def parse_iso_date_str(s):
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")


def number_to_dollars(n):
    return "${0:,.2f}".format(n)
