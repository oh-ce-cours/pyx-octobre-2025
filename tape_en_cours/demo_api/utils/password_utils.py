import os
import getpass
from .logging_config import get_logger

# Logger pour ce module
logger = get_logger(__name__)


def get_password(prompt="Mot de passe: ", env_var="DEMO_API_PASSWORD"):
    """
    Récupère un mot de passe depuis une variable d'environnement ou demande une saisie sécurisée.

    Args:
        prompt (str): Message à afficher lors de la saisie manuelle
        env_var (str): Nom de la variable d'environnement contenant le mot de passe

    Returns:
        str: Le mot de passe récupéré
    """
    # Essayer de récupérer depuis une variable d'environnement
    password_from_env = os.environ.get(env_var)

    if password_from_env:
        print(f"Mot de passe récupéré depuis la variable d'environnement '{env_var}'")
        return password_from_env

    # Si pas de variable d'environnement, demander une saisie sécurisée
    print("Aucune variable d'environnement trouvée. Saisie sécurisée nécessaire.")
    password = getpass.getpass(prompt=prompt)

    if not password:
        raise ValueError("Le mot de passe ne peut pas être vide")

    return password


def get_credentials(
    email=None, env_email="DEMO_API_EMAIL", env_password="DEMO_API_PASSWORD"
):
    """
    Récupère les identifiants (email et mot de passe) depuis les variables d'environnement
    ou demande une saisie interactive.

    Args:
        email (str, optional): Email à utiliser (priorité sur la variable d'environnement)
        env_email (str): Nom de la variable d'environnement pour l'email
        env_password (str): Nom de la variable d'environnement pour le mot de passe

    Returns:
        tuple: (email, password)
    """
    # Récupérer l'email
    if email:
        user_email = email
    else:
        user_email = os.environ.get(env_email)
        if not user_email:
            user_email = input(f"Email (ou définir {env_email}): ").strip()

    # Récupérer le mot de passe
    password = get_password(env_var=env_password)

    return user_email, password
