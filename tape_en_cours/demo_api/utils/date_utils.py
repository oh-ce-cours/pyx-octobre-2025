"""
Utilitaires pour la manipulation des dates et timestamps.

Ce module fournit des fonctions utilitaires pour convertir
et manipuler les timestamps Unix utilisés par l'API.
"""

import datetime


def parse_unix_timestamp(ts):
    """
    Convertit un timestamp Unix (en millisecondes) en objet datetime.

    Args:
        ts (int): Timestamp Unix en millisecondes

    Returns:
        datetime.datetime: Objet datetime correspondant

    Example:
        >>> parse_unix_timestamp(1640995200000)
        datetime.datetime(2022, 1, 1, 0, 0)
    """
    return datetime.datetime.fromtimestamp(ts / 1e3)
