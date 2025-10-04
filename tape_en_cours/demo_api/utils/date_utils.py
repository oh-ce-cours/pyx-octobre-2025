import datetime


def parse_unix_timestamp(ts):
    """Convertit un timestamp Unix (en millisecondes) en objet datetime."""
    return datetime.datetime.fromtimestamp(ts / 1e3)
