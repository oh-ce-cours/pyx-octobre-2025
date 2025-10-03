import datetime


def parse_unix_timestamp(ts):
    return datetime.datetime.fromtimestamp(ts / 1e3)
