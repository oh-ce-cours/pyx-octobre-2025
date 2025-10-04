"""
Exceptions personnalisées pour l'API demo_api

Ce module définit toutes les exceptions spécifiques à l'API,
permettant une gestion d'erreurs plus claire et plus robuste.
"""

from typing import Optional, Dict, Any


class DemoAPIException(Exception):
    """Exception de base pour toutes les erreurs de l'API demo_api"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}

    def __str__(self) -> str:
        base_msg = self.message
        if self.status_code:
            base_msg += f" (Status: {self.status_code})"
        return base_msg


class AuthenticationError(DemoAPIException):
    """Exception levée lors d'erreurs d'authentification"""

    def __init__(
        self,
        message: str = "Erreur d'authentification",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, status_code, response_data)


class UserCreationError(DemoAPIException):
    """Exception levée lors d'erreurs de création d'utilisateur"""

    def __init__(
        self,
        message: str = "Erreur lors de la création d'utilisateur",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        email: Optional[str] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.email = email


class UserLoginError(DemoAPIException):
    """Exception levée lors d'erreurs de connexion utilisateur"""

    def __init__(
        self,
        message: str = "Erreur lors de la connexion utilisateur",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        email: Optional[str] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.email = email


class UserInfoError(DemoAPIException):
    """Exception levée lors d'erreurs de récupération d'informations utilisateur"""

    def __init__(
        self,
        message: str = "Erreur lors de la récupération des informations utilisateur",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        token_length: Optional[int] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.token_length = token_length


class UsersFetchError(DemoAPIException):
    """Exception levée lors d'erreurs de récupération des utilisateurs"""

    def __init__(
        self,
        message: str = "Erreur lors de la récupération des utilisateurs",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        base_url: Optional[str] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.base_url = base_url


class VMsFetchError(DemoAPIException):
    """Exception levée lors d'erreurs de récupération des VMs"""

    def __init__(
        self,
        message: str = "Erreur lors de la récupération des VMs",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        base_url: Optional[str] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.base_url = base_url


class VMCreationError(DemoAPIException):
    """Exception levée lors d'erreurs de création de VM"""

    def __init__(
        self,
        message: str = "Erreur lors de la création de VM",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        user_id: Optional[int] = None,
        vm_name: Optional[str] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.user_id = user_id
        self.vm_name = vm_name


class TokenError(DemoAPIException):
    """Exception levée lors d'erreurs liées aux tokens"""

    def __init__(
        self,
        message: str = "Erreur liée au token",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        token_length: Optional[int] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.token_length = token_length


class CredentialsError(DemoAPIException):
    """Exception levée lors d'erreurs liées aux identifiants"""

    def __init__(
        self,
        message: str = "Erreur liée aux identifiants",
        email: Optional[str] = None,
        password_provided: bool = False,
    ):
        super().__init__(message)
        self.email = email
        self.password_provided = password_provided


class NetworkError(DemoAPIException):
    """Exception levée lors d'erreurs réseau"""

    def __init__(
        self,
        message: str = "Erreur réseau",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        url: Optional[str] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.url = url


class UserUpdateError(DemoAPIException):
    """Exception levée lors d'erreurs de mise à jour d'utilisateur"""

    def __init__(
        self,
        message: str = "Erreur lors de la mise à jour de l'utilisateur",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        user_id: Optional[int] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.user_id = user_id


class UserDeleteError(DemoAPIException):
    """Exception levée lors d'erreurs de suppression d'utilisateur"""

    def __init__(
        self,
        message: str = "Erreur lors de la suppression de l'utilisateur",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        user_id: Optional[int] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.user_id = user_id


class VMUpdateError(DemoAPIException):
    """Exception levée lors d'erreurs de mise à jour de VM"""

    def __init__(
        self,
        message: str = "Erreur lors de la mise à jour de la VM",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        vm_id: Optional[int] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.vm_id = vm_id


class VMDeleteError(DemoAPIException):
    """Exception levée lors d'erreurs de suppression de VM"""

    def __init__(
        self,
        message: str = "Erreur lors de la suppression de la VM",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        vm_id: Optional[int] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.vm_id = vm_id


class APIRequestError(DemoAPIException):
    """Exception levée lors d'erreurs génériques de requêtes API"""

    def __init__(
        self,
        message: str = "Erreur lors de la requête API",
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        endpoint: Optional[str] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.endpoint = endpoint
