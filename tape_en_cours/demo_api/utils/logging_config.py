"""Configuration du logging avec structlog pour demo_api"""

import structlog
import sys
import os


def setup_logging():
    """
    Configure structlog avec un format JSON joli et structuré.
    """
    # Configuration de la sortie selon l'environnement via le gestionnaire de config
    from .config import config
    
    debug_mode = config.DEMO_API_DEBUG
    log_level = config.DEMO_API_LOG_LEVEL

    # Configuration des processeurs
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # Configuration pour la console (format humain)
    console_processors = processors + [
        structlog.dev.ConsoleRenderer(colors=sys.stdout.isatty())
    ]

    # Configuration selon le niveau de détail souhaité
    if debug_mode:
        # Mode debug : plus de détails
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
