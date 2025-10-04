#!/usr/bin/env python3
"""
Gestionnaire de VMs pour demo_api
"""

import typer
from typing import Optional
from utils.api import Api
from utils.services import VMService
from utils.logging_config import get_logger
from utils.config import config

logger = get_logger(__name__)


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

    # Initialisation du client API et du service
    api = Api(config.DEMO_API_BASE_URL)
    vm_service = VMService(api)

    # Authentification de l'utilisateur
    typer.echo("🔐 Authentification de l'utilisateur...")
    user = vm_service.authenticate_user(email=email, password=config.DEMO_API_PASSWORD)

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
    vm_result = vm_service.create_vm_for_user(user, vm_config)

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
