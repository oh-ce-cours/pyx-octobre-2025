import os
import getpass
from .logging_config import get_logger

# Logger pour ce module
logger = get_logger(__name__)


def get_password_from_env(env_var="DEMO_API_PASSWORD"):
    """
    Récupère un mot de passe depuis une variable d'environnement uniquement.

    Args:
        env_var (str): Nom de la variable d'environnement contenant le mot de passe

    Returns:
        str|None: Le mot de passe récupéré ou None si pas trouvé
    """
    password = os.environ.get(env_var)

    if password:
        logger.info(
            "Mot de passe récupéré depuis la variable d'environnement",
            env_var=env_var,
            password_length=len(password),
        )
    else:
        logger.debug(
            "Aucun mot de passe trouvé dans les variables d'environnement",
            env_var=env_var,
        )

    return password


def get_password_from_input(prompt="Mot de passe: "):
    """
    Demande une saisie sécurisée de mot de passe à l'utilisateur.

    Args:
        prompt (str): Message à afficher lors de la saisie

    Returns:
        str: Le mot de passe saisi

    Raises:
        ValueError: Si le mot de passe est vide
    """
    logger.info("Demande de saisie sécurisée de mot de passe")
    password = getpass.getpass(prompt=prompt)

    if not password:
        logger.error("Erreur: mot de passe vide fourni")
        raise ValueError("Le mot de passe ne peut pas être vide")

    logger.info("Mot de passe saisi avec succès", password_length=len(password))
    return password


def get_password(prompt="Mot de passe: ", env_var="DEMO_API_PASSWORD"):
    """
    Récupère un mot de passe depuis une variable d'environnement ou demande une saisie sécurisée.
    Fonction de compatibilité qui combine les deux méthodes.

    Args:
        prompt (str): Message à afficher lors de la saisie manuelle
        env_var (str): Nom de la variable d'environnement contenant le mot de passe

    Returns:
        str: Le mot de passe récupéré
    """
    logger.info("Récupération du mot de passe", env_var=env_var)

    # Essayer d'abord depuis les variables d'environnement
    password = get_password_from_env(env_var)

    if password:
        return password

    # Si pas de variable d'environnement, demander une saisie sécurisée
    logger.warning(
        "Aucune variable d'environnement trouvée. Saisie sécurisée nécessaire.",
        env_var=env_var,
    )
    return get_password_from_input(prompt)


def get_email_from_env(env_var="DEMO_API_EMAIL"):
    """
    Récupère l'email depuis une variable d'environnement uniquement.

    Args:
        env_var (str): Nom de la variable d'environnement pour l'email

    Returns:
        str|None: L'email récupéré ou None si pas trouvé
    """
    email = os.environ.get(env_var)

    if email:
        logger.info(
            "Email récupéré depuis la variable d'environnement",
            email=email,
            env_var=env_var,
        )
    else:
        logger.debug(
            "Aucun email trouvé dans les variables d'environnement", env_var=env_var
        )

    return email


def get_email_from_input(env_var="DEMO_API_EMAIL"):
    """
    Demande la saisie de l'email à l'utilisateur.

    Args:
        env_var (str): Nom de la variable d'environnement pour l'aide

    Returns:
        str: L'email saisi
    """
    logger.info("Demande de saisie d'email")
    email = input(f"Email (ou définir {env_var}): ").strip()

    if not email:
        logger.error("Erreur: email vide fourni")
        raise ValueError("L'email ne peut pas être vide")

    logger.info("Email saisi avec succès", email=email)
    return email


def get_credentials_from_env(
    env_email="DEMO_API_EMAIL", env_password="DEMO_API_PASSWORD"
):
    """
    Récupère les identifiants depuis les variables d'environnement uniquement.

    Args:
        env_email (str): Nom de la variable d'environnement pour l'email
        env_password (str): Nom de la variable d'environnement pour le mot de passe

    Returns:
        tuple|None: (email, password) ou None si incomplet
    """
    logger.info("Récupération des identifiants depuis les variables d'environnement")

    email = get_email_from_env(env_email)
    password = get_password_from_env(env_password)

    if email and password:
        logger.info(
            "Identifiants récupérés depuis les variables d'environnement", email=email
        )
        return email, password
    else:
        logger.warning(
            "Identifiants incomplets dans les variables d'environnement",
            email_found=bool(email),
            password_found=bool(password),
        )
        return None


def get_credentials_from_input(
    env_email="DEMO_API_EMAIL", env_password="DEMO_API_PASSWORD"
):
    """
    Demande la saisie interactive des identifiants.

    Args:
        env_email (str): Nom de la variable d'environnement pour l'aide
        env_password (str): Nom de la variable d'environnement pour l'aide

    Returns:
        tuple: (email, password)
    """
    logger.info("Saisie interactive des identifiants")

    email = get_email_from_input(env_email)
    password = get_password_from_input()

    logger.info("Identifiants saisis avec succès", email=email)
    return email, password


def get_credentials(
    email=None, env_email="DEMO_API_EMAIL", env_password="DEMO_API_PASSWORD"
):
    """
    Récupère les identifiants (email et mot de passe) depuis les variables d'environnement
    ou demande une saisie interactive. Fonction de compatibilité qui combine les méthodes.

    Args:
        email (str, optional): Email à utiliser (priorité sur la variable d'environnement)
        env_email (str): Nom de la variable d'environnement pour l'email
        env_password (str): Nom de la variable d'environnement pour le mot de passe

    Returns:
        tuple: (email, password)
    """
    logger.info(
        "Récupération des identifiants", email_provided=bool(email), env_email=env_email
    )

    # Si email fourni directement, utiliser seulement le mot de passe
    if email:
        logger.info("Email fourni directement", email=email)
        password = get_password(env_var=env_password)
        logger.info(
            "Identifiants récupérés avec succès", email=email, password_source="mixed"
        )
        return email, password

    # Essayer d'abord depuis les variables d'environnement
    credentials = get_credentials_from_env(env_email, env_password)
    if credentials:
        return credentials

    # Si incomplet, demander une saisie interactive
    logger.warning(
        "Identifiants incomplets dans les variables d'environnement. Saisie interactive nécessaire."
    )
    return get_credentials_from_input(env_email, env_password)
