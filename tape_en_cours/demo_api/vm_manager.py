#!/usr/bin/env python3
"""
Gestionnaire de VMs pour demo_api
"""

import typer
from typing import Optional, Dict, Any
from utils.api import Api
from utils.api.exceptions import (
    VMCreationError,
    UsersFetchError,
    UserInfoError,
    TokenError,
)
from utils.logging_config import get_logger
from utils.config import config
from utils.password_utils import get_or_create_token

logger = get_logger(__name__)


def authenticate_user(api: Api, email: str = "jean@dupont21.com", password: str = None) -> Optional[Dict[str, Any]]:
    """
    Authentifie un utilisateur et retourne ses informations

    Args:
        api: Client API unifié
        email: Email de l'utilisateur
        password: Mot de passe de l'utilisateur

    Returns:
        Informations de l'utilisateur ou None si l'authentification échoue
    """
    logger.info("Début du processus d'authentification pour création de VM")

    try:
        token = get_or_create_token(
            base_url=api.base_url,
            email=email,
            password=password,
            token_env_var="DEMO_API_TOKEN",
        )

        # Définir le token dans le client API
        api.set_token(token)
        logger.info("Token défini dans le client API pour création de VM")

        # Récupérer les informations utilisateur
        if api.is_authenticated():
            logger.info("Récupération des informations utilisateur authentifié")
            try:
                user = api.get_user_info()
                logger.info(
                    "Informations utilisateur récupérées pour création VM",
                    user_id=user.get("id"),
                    user_name=user.get("name"),
                )
                return user
            except UserInfoError as e:
                logger.error(
                    "Impossible de récupérer les informations utilisateur",
                    error=str(e),
                )
                return None
        else:
            logger.error("Aucun token disponible après authentification")
            return None

    except Exception as e:
        logger.error("Erreur d'authentification", error=str(e))
        return None


def create_vm_for_user(api: Api, user: Dict[str, Any], vm_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Crée une VM pour un utilisateur spécifique

    Args:
        api: Client API unifié
        user: Informations de l'utilisateur
        vm_config: Configuration de la VM à créer

    Returns:
        Résultat de la création ou None si échec
    """
    if not api.is_authenticated():
        logger.error("API non authentifiée pour la création de VM")
        return None

    logger.info("Début de création de VM", **vm_config)

    try:
        vm_result = api.users.create_vm(**vm_config)
        logger.info(
            "VM créée avec succès",
            vm_id=vm_result.get("id"),
            status=vm_config.get("status"),
        )
        return vm_result
    except VMCreationError as e:
        logger.error("Échec de la création de VM", error=str(e), user_id=user["id"])
        return None


def create_default_vm_for_user(api: Api, user: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Crée une VM par défaut pour un utilisateur

    Args:
        api: Client API unifié
        user: Informations de l'utilisateur

    Returns:
        Résultat de la création ou None si échec
    """
    vm_config = {
        "user_id": user["id"],
        "name": "VM de Jean",
        "operating_system": "Ubuntu 22.04",
        "cpu_cores": 2,
        "ram_gb": 4,
        "disk_gb": 50,
        "status": "stopped",
    }

    return create_vm_for_user(api, user, vm_config)


def create_vm(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Nom de la VM"),
    email: str = typer.Option(
        "jean@dupont21.com", "--email", "-e", help="Email de l'utilisateur"
    ),
    os: str = typer.Option("Ubuntu 22.04", "--os", "-o", help="Système d'exploitation"),
    cores: int = typer.Option(
        2, "--cores", "-c", help="Nombre de cœurs CPU", min=1, max=16
    ),
    ram: int = typer.Option(4, "--ram", "-r", help="RAM en GB", min=1, max=128),
    disk: int = typer.Option(50, "--disk", "-d", help="Disque en GB", min=10, max=2048),
    status: str = typer.Option(
        "stopped", "--status", "-s", help="Statut initial de la VM"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    🖥️ Créer une VM

    Exemples:

    \b
    python vm_manager.py create
    python vm_manager.py create --name "Ma VM" --cores 4
    python vm_manager.py create -n "VM Test" --ram 8 --disk 100 --verbose
    """

    # Configurer le nom par défaut si non fourni
    vm_name = name or "VM de Jean"

    if verbose:
        typer.echo("🔧 Configuration VM:")
        typer.echo(f"   Nom: {vm_name}")
        typer.echo(f"   OS: {os}")
        typer.echo(f"   CPU: {cores} cores")
        typer.echo(f"   RAM: {ram} GB")
        typer.echo(f"   Disque: {disk} GB")
        typer.echo(f"   Statut: {status}")
        typer.echo(f"   Email: {email}")
        typer.echo()

    logger.info("Début du processus de création de VM", email=email, vm_name=vm_name)

    # Initialisation du client API
    api = Api(config.DEMO_API_BASE_URL)

    # Authentification de l'utilisateur
    typer.echo("🔐 Authentification de l'utilisateur...")
    user = authenticate_user(api, email=email, password=config.DEMO_API_PASSWORD)

    if not user:
        typer.echo("❌ Échec de l'authentification")
        raise typer.Exit(1)

    typer.echo(f"✅ Utilisateur authentifié: {user.get('name', email)}")

    # Configuration de la VM
    vm_config = {
        "user_id": user["id"],
        "name": vm_name,
        "operating_system": os,
        "cpu_cores": cores,
        "ram_gb": ram,
        "disk_gb": disk,
        "status": status,
    }

    if verbose:
        typer.echo("🚀 Création de la VM...")

    # Création de la VM
    logger.info("Création de la VM", **vm_config)
    vm_result = create_vm_for_user(api, user, vm_config)

    typer.echo()
    if vm_result:
        typer.echo("🎉 VM créée avec succès!")
        typer.echo(f"   🆔 ID: {vm_result.get('id')}")
        typer.echo(f"   📝 Nom: {vm_result.get('name')}")
        typer.echo(f"   💻 OS: {vm_result.get('operating_system')}")
        typer.echo(f"   🔧 CPU: {vm_result.get('cpu_cores')} cores")
        typer.echo(f"   💾 RAM: {vm_result.get('ram_gb')} GB")
        typer.echo(f"   💿 Disque: {vm_result.get('disk_gb')} GB")
        typer.echo(f"   ⚡ Statut: {vm_result.get('status')}")
        typer.echo()
        typer.echo("✨ Terminé!")
    else:
        typer.echo("❌ Échec de la création de la VM")
        raise typer.Exit(1)


if __name__ == "__main__":
    app = typer.Typer(help="Créer des VMs pour l'API demo")
    app.command()(create_vm)
    app()
