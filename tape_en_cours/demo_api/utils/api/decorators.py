"""
Décorateurs spécifiques aux appels API.
"""

import time
from functools import wraps
from typing import Callable
from utils.logging_config import get_logger
from utils.config import Config

# Logger pour ce module
logger = get_logger(__name__)

# Configuration centralisée
config = Config()


def retry_on_429(max_retries: int = None, base_delay: float = 7.0):
    """
    Décorateur pour gérer automatiquement les erreurs 429 (Too Many Requests)
    avec retry et backoff exponentiel.

    Args:
        max_retries: Nombre maximum de tentatives (défaut: 5)
        base_delay: Délai de base en secondes (défaut: 2.0)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            # Utiliser la configuration si max_retries n'est pas spécifié
            actual_max_retries = max_retries if max_retries is not None else config.DEMO_API_MAX_RETRIES

            for attempt in range(actual_max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    error_str = str(e).lower()

                    # Si c'est une erreur 429 (Too Many Requests), on retry avec backoff
                    if "429" in error_str and "too many requests" in error_str:
                        if attempt < max_retries:
                            # Backoff exponentiel avec délai maximum de 30s
                            delay = min(base_delay * (2**attempt), 30.0)
                            logger.warning(
                                f"Limite API atteinte pour {func.__name__}, "
                                f"attente {delay:.1f}s avant retry {attempt + 1}/{max_retries}"
                            )
                            time.sleep(delay)
                            continue
                    else:
                        # Pour les autres erreurs, on ne retry pas
                        raise e

            # Si on arrive ici, toutes les tentatives ont échoué
            raise last_exception

        return wrapper

    return decorator
