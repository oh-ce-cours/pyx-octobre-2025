import datetime


def parse_unix_timestamp(ts):
    """Convertit un timestamp Unix (en millisecondes) en objet datetime."""
    return datetime.datetime.fromtimestamp(ts / 1e3)


def format_timestamp_for_display(timestamp):
    """Formate un timestamp pour l'affichage utilisateur.
    
    Args:
        timestamp: Timestamp Unix (int/float) ou objet datetime
        
    Returns:
        str: Date formatée en français (ex: "04/10/2025 à 17:15:25")
    """
    if timestamp is None:
        return "N/A"
    
    if isinstance(timestamp, (int, float)):
        # Timestamp Unix en millisecondes
        dt = parse_unix_timestamp(timestamp)
    elif isinstance(timestamp, datetime.datetime):
        # Objet datetime déjà converti
        dt = timestamp
    else:
        # Chaîne ou autre format
        return str(timestamp)
    
    return dt.strftime("%d/%m/%Y à %H:%M:%S")


def get_current_timestamp():
    """Retourne le timestamp Unix actuel en millisecondes."""
    return int(datetime.datetime.now().timestamp() * 1000)
