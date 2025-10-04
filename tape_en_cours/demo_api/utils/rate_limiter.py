"""
Gestionnaire de rate limiting pour respecter les limites de l'API
"""

import time
import asyncio
from typing import Optional, Callable, Any
from functools import wraps
from utils.logging_config import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """Gestionnaire de rate limiting pour les appels API"""

    def __init__(self, max_requests: int = 10, time_window: int = 20):
        """
        Initialise le rate limiter

        Args:
            max_requests: Nombre maximum de requêtes par fenêtre de temps
            time_window: Fenêtre de temps en secondes
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self._lock = asyncio.Lock()

        logger.info(
            "Rate limiter initialisé",
            max_requests=max_requests,
            time_window=time_window,
        )

    async def wait_if_needed(self) -> None:
        """Attend si nécessaire pour respecter les limites de rate"""
        async with self._lock:
            now = time.time()

            # Nettoyer les requêtes anciennes
            self.requests = [
                req_time
                for req_time in self.requests
                if now - req_time < self.time_window
            ]

            # Si on a atteint la limite, attendre
            if len(self.requests) >= self.max_requests:
                oldest_request = min(self.requests)
                wait_time = self.time_window - (now - oldest_request) + 0.1

                if wait_time > 0:
                    logger.info(
                        "Rate limit atteint, attente",
                        wait_time=wait_time,
                        current_requests=len(self.requests),
                    )
                    await asyncio.sleep(wait_time)

                    # Nettoyer à nouveau après l'attente
                    now = time.time()
                    self.requests = [
                        req_time
                        for req_time in self.requests
                        if now - req_time < self.time_window
                    ]

            # Enregistrer cette requête
            self.requests.append(now)
            logger.debug(
                "Requête autorisée",
                current_requests=len(self.requests),
                max_requests=self.max_requests,
            )


class RateLimitedClient:
    """Client avec rate limiting intégré"""

    def __init__(self, rate_limiter: Optional[RateLimiter] = None):
        """
        Initialise le client avec rate limiting

        Args:
            rate_limiter: Instance du rate limiter (créé automatiquement si None)
        """
        self.rate_limiter = rate_limiter or RateLimiter()

    def rate_limit(self, func: Callable) -> Callable:
        """Décorateur pour appliquer le rate limiting à une fonction"""

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            await self.rate_limiter.wait_if_needed()
            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Pour les fonctions synchrones, on utilise asyncio.run
            async def async_func():
                await self.rate_limiter.wait_if_needed()
                return func(*args, **kwargs)

            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Si on est déjà dans un event loop, créer une tâche
                    import concurrent.futures

                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, async_func())
                        return future.result()
                else:
                    return asyncio.run(async_func())
            except RuntimeError:
                # Pas d'event loop, en créer un nouveau
                return asyncio.run(async_func())

        # Détecter si la fonction est async
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper


# Instance globale du rate limiter
_global_rate_limiter = RateLimiter()


def rate_limit(max_requests: int = 10, time_window: int = 20):
    """
    Décorateur pour appliquer le rate limiting à une fonction

    Args:
        max_requests: Nombre maximum de requêtes par fenêtre de temps
        time_window: Fenêtre de temps en secondes
    """

    def decorator(func: Callable) -> Callable:
        rate_limiter = RateLimiter(max_requests, time_window)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            await rate_limiter.wait_if_needed()
            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            async def async_func():
                await rate_limiter.wait_if_needed()
                return func(*args, **kwargs)

            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    import concurrent.futures

                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, async_func())
                        return future.result()
                else:
                    return asyncio.run(async_func())
            except RuntimeError:
                return asyncio.run(async_func())

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def get_global_rate_limiter() -> RateLimiter:
    """Retourne l'instance globale du rate limiter"""
    return _global_rate_limiter
