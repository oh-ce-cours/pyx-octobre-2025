"""Configuration du logging avec structlog pour demo_api"""

import structlog
import sys
import os


# Configuration des processeurs structlog
def customize_logging_format(_, method_name, event_dict):
    """
    Personnalise le format des logs avec des informations supplémentaires.
    """
    # Ajouter le timestamp si pas présent
    if "timestamp" not in event_dict:
        from datetime import datetime

        event_dict["timestamp"] = datetime.utcnow().isoformat() + "Z"

    # Ajouter le niveau de log de manière plus claire
    event_dict["level"] = method_name.upper()

    # Ajouter des métadonnées utiles
    event_dict["app"] = "demo_api"

    return event_dict


def setup_logging():
    """
    Configure structlog avec un format JSON joli et structuré.
    """
    # Configuration de la sortie selon l'environnement
    debug_mode = os.environ.get("DEMO_API_DEBUG", "false").lower() == "true"
    log_level = os.environ.get("DEMO_API_LOG_LEVEL", "DEBUG" if debug_mode else "INFO")

    # Configuration des processeurs
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        customize_logging_format,
    ]

    # Configuration pour la console (format humain)
    console_processors = processors + [
        structlog.dev.ConsoleRenderer(colors=sys.stdout.isatty())
    ]

    # Configuration selon le niveau de détail souhaité
    if debug_mode:
        # Mode debug : plus de détails
        processors.append(structlog.processors.dict_tracebacks)
        console_processors.append(structlog.processors.dict_tracebacks)

    # Configuration structlog
    structlog.configure(
        processors=console_processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return log_level


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Retourne un logger configuré avec structlog.

    Args:
        name: Nom du logger (généralement __name__ du module appelant)

    Returns:
        Logger configuré avec structlog
    """
    setup_logging()
    return structlog.get_logger(name)


# Mise en place d'un logger par défaut pour l'application
application_logger = get_logger(__name__)
