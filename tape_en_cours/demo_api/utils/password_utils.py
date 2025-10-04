import os
import getpass
from .logging_config import get_logger
from .api.exceptions import CredentialsError, TokenError

# Logger pour ce module
logger = get_logger(__name__)


def get_password_from_config():
    """
    Récupère le mot de passe depuis le gestionnaire de configuration.

    Returns:
        str|None: Le mot de passe récupéré ou None si pas trouvé
    """
    from .config import config

    password = config.DEMO_API_PASSWORD

    if password:
        logger.info(
            "Mot de passe récupéré depuis le gestionnaire de configuration",
            password_length=len(password),
        )
    else:
        logger.debug(
            "Aucun mot de passe trouvé dans la configuration",
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


def get_password(prompt="Mot de passe: "):
    """
    Récupère un mot de passe depuis la configuration ou demande une saisie sécurisée.

    Args:
        prompt (str): Message à afficher lors de la saisie manuelle

    Returns:
        str: Le mot de passe récupéré
    """
    logger.info("Récupération du mot de passe")

    # Essayer d'abord depuis la configuration
    password = get_password_from_config()

    if password:
        return password

    # Si pas de configuration, demander une saisie sécurisée
    logger.warning(
        "Aucun mot de passe trouvé dans la configuration. Saisie sécurisée nécessaire.",
    )
    return get_password_from_input(prompt)


def get_email_from_config():
    """
    Récupère l'email depuis le gestionnaire de configuration.

    Returns:
        str|None: L'email récupéré ou None si pas trouvé
    """
    from .config import config

    email = config.DEMO_API_EMAIL

    if email:
        logger.info(
            "Email récupéré depuis le gestionnaire de configuration",
            email=email,
        )
    else:
        logger.debug(
            "Aucun email trouvé dans la configuration",
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


def get_credentials_from_config():
    """
    Récupère les identifiants depuis le gestionnaire de configuration.

    Returns:
        tuple|None: (email, password) ou None si incomplet
    """
    logger.info("Récupération des identifiants depuis le gestionnaire de configuration")

    email = get_email_from_config()
    password = get_password_from_config()

    if email and password:
        logger.info(
            "Identifiants récupérés depuis le gestionnaire de configuration",
            email=email,
        )
        return email, password
    else:
        logger.warning(
            "Identifiants incomplets dans la configuration",
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


def get_credentials(email=None):
    """
    Récupère les identifiants (email et mot de passe) depuis la configuration
    ou demande une saisie interactive.

    Args:
        email (str, optional): Email à utiliser (priorité sur la configuration)

    Returns:
        tuple: (email, password)
    """
    logger.info("Récupération des identifiants", email_provided=bool(email))

    # Si email fourni directement, utiliser seulement le mot de passe
    if email:
        logger.info("Email fourni directement", email=email)
        password = get_password()
        logger.info(
            "Identifiants récupérés avec succès", email=email, password_source="mixed"
        )
        return email, password

    # Essayer d'abord depuis la configuration
    credentials = get_credentials_from_config()
    if credentials:
        return credentials

    # Si incomplet, demander une saisie interactive
    logger.warning(
        "Identifiants incomplets dans la configuration. Saisie interactive nécessaire."
    )
    return get_credentials_from_input()


# === Gestion des tokens d'authentification ===


def get_token_from_config():
    """
    Récupère un token d'authentification depuis le gestionnaire de configuration.

    Returns:
        str|None: Le token récupéré ou None si pas trouvé
    """
    from .config import config
    
    token = config.DEMO_API_TOKEN

    if token:
        logger.info(
            "Token d'authentification récupéré depuis le gestionnaire de configuration",
            token_length=len(token),
        )
    else:
        logger.debug(
            "Aucun token trouvé dans la configuration",
        )

    return token


def save_token_to_env(token, env_var="DEMO_API_TOKEN"):
    """
    Sauvegarde un token en utilisant le gestionnaire de configuration.

    Args:
        token (str): Le token à sauvegarder
        env_var (str): Nom de la variable d'environnement

    Returns:
        bool: True si sauvegardé avec succès
    """
    if not token:
        logger.error("Impossible de sauvegarder un token vide")
        return False

    # Utiliser le gestionnaire de configuration pour sauvegarder
    from .config import config

    if env_var == "DEMO_API_TOKEN":
        success = config.update_token(token)
    else:
        success = config.save_to_env_file(env_var, token)

    if success:
        logger.info(
            "Token sauvegardé avec succès via le gestionnaire de configuration",
            env_var=env_var,
            token_length=len(token),
        )
    else:
        logger.warning(
            "Impossible de sauvegarder le token via le gestionnaire de configuration",
            env_var=env_var,
        )

    return success


def remove_token_from_env(env_var="DEMO_API_TOKEN"):
    """
    Supprime un token des variables d'environnement (session uniquement).

    Args:
        env_var (str): Nom de la variable d'environnement

    Returns:
        bool: True si supprimé avec succès
    """
    if env_var in os.environ:
        del os.environ[env_var]
        logger.info(
            "Token supprimé des variables d'environnement de la session",
            env_var=env_var,
        )
        return True
    else:
        logger.debug(
            "Token non trouvé dans les variables d'environnement", env_var=env_var
        )
        return False


def get_or_create_token(
    base_url, email=None, password=None, token_env_var="DEMO_API_TOKEN"
):
    """
    Récupère un token depuis les variables d'environnement ou en crée un nouveau.

    Args:
        base_url (str): URL de base de l'API
        email (str|None): Email pour l'authentification
        password (str|None): Mot de passe pour l'authentification
        token_env_var (str): Variable d'environnement pour le token

    Returns:
        str: Token valide

    Raises:
        CredentialsError: Si les identifiants sont invalides
        TokenError: Si la création/récupération du token échoue
    """
    from .api.auth import Auth, UserCreationError, UserLoginError, UserInfoError

    # Essayer d'abord de récupérer depuis les variables d'environnement
    existing_token = get_token_from_env(token_env_var)
    if existing_token:
        logger.info("Token existant trouvé dans les variables d'environnement")

        # Tester si le token est encore valide
        auth = Auth(base_url)
        try:
            user_info = auth.get_logged_user_info(existing_token)
            logger.info(
                "Token existant validé avec succès", user_id=user_info.get("id")
            )
            return existing_token
        except UserInfoError:
            logger.warning(
                "Token existant expiré ou invalide, nouvelle authentification nécessaire"
            )
            remove_token_from_env(token_env_var)

    # Créer un nouveau token
    logger.info("Création d'un nouveau token d'authentification")

    # Récupérer les identifiants si non fournis
    if not email or not password:
        try:
            email, password = get_credentials(email=email)
        except ValueError as e:
            raise CredentialsError(
                f"Erreur lors de la récupération des identifiants: {str(e)}"
            )

    # Authentification
    auth = Auth(base_url)

    # Essayer de créer un utilisateur, sinon se connecter
    try:
        token = auth.create_user("Demo User", email, password)
        logger.info("Nouvel utilisateur créé avec succès", email=email)
    except UserCreationError as e:
        if "Utilisateur déjà existant" in str(e):
            logger.warning(
                "Utilisateur déjà existant, tentative de connexion", email=email
            )
            try:
                token = auth.login_user(email, password)
            except UserLoginError as login_error:
                raise CredentialsError(
                    f"Impossible de se connecter avec l'email {email}: {str(login_error)}",
                    email=email,
                    password_provided=bool(password),
                )
        else:
            raise TokenError(f"Impossible de créer l'utilisateur {email}: {str(e)}")

    # Sauvegarder le token pour les prochaines utilisations
    save_token_to_env(token, token_env_var)
    logger.info("Nouveau token créé et sauvegardé", email=email)
    return token


# === Utilitaires pour fichier .env ===


def save_token_to_env_file(token, env_file_path=".env", token_key="DEMO_API_TOKEN"):
    """
    Sauvegarde un token dans un fichier .env en utilisant python-dotenv.

    Args:
        token (str): Token à sauvegarder
        env_file_path (str): Chemin vers le fichier .env
        token_key (str): Clé pour le token dans le fichier

    Returns:
        bool: True si sauvegardé avec succès
    """
    if not token:
        logger.error("Impossible de sauvegarder un token vide")
        return False

    try:
        # Utiliser python-dotenv pour sauvegarder
        set_key(env_file_path, token_key, token)

        logger.info(
            "Token sauvegardé dans le fichier .env",
            env_file=env_file_path,
            token_key=token_key,
            token_length=len(token),
        )
        return True

    except Exception as e:
        logger.error(
            "Erreur lors de la sauvegarde du token dans .env",
            error=str(e),
            env_file=env_file_path,
        )
        return False


def load_token_from_env_file(env_file_path=".env", token_key="DEMO_API_TOKEN"):
    """
    Charge un token depuis un fichier .env en utilisant python-dotenv.

    Args:
        env_file_path (str): Chemin vers le fichier .env
        token_key (str): Clé pour le token dans le fichier

    Returns:
        str|None: Token chargé ou None si non trouvé/erreur
    """
    try:
        # Charger le fichier .env spécifique
        loaded = load_dotenv(env_file_path)

        if not loaded:
            logger.debug("Fichier .env non trouvé", env_file=env_file_path)
            return None

        # Récupérer la valeur depuis les variables d'environnement (maintenant chargées)
        token = os.environ.get(token_key)

        if token:
            logger.info(
                "Token chargé depuis le fichier .env",
                env_file=env_file_path,
                token_key=token_key,
                token_length=len(token),
            )
        else:
            logger.debug(
                "Token non trouvé dans le fichier .env",
                env_file=env_file_path,
                token_key=token_key,
            )

        return token

    except Exception as e:
        logger.error(
            "Erreur lors du chargement du token depuis .env",
            error=str(e),
            env_file=env_file_path,
        )
        return None
