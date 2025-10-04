#!/usr/bin/env python3
"""
Script de création de VM

Ce script authentifie un utilisateur et crée une VM selon la configuration spécifiée.
"""

import sys
import typer
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.api import Api
from utils.services import VMService
from utils.logging_config import get_logger
from utils.config import config

logger = get_logger("create_vm")
app = typer.Typer(help="Créer une VM pour un utilisateur")


def create_vm(
    email: str = typer.Option("jean@dupont21.com", "--email", "-e", help="Email de l'utilisateur"),
    name: str = typer.Option("VM de Jean", "--name", "-n", help="Nom de la VM"),
    os: str = typer.Option("Ubuntu 22.04", "--os", "-o", help="Système d'exploitation"),
    cores: int = typer.Option(2, "--cores", "-c", help="Nombre de cœurs CPU", min=1, max=16),
    ram: int = typer.Option(4, "--ram", "-r", help="RAM en GB", min=1, max=128),
    disk: int = typer.Option(50, "--disk", "-d", help="Disque en GB", min=10, max=2048),
    status: str = typer.Option("stopped", "--status", "-s", help="Statut initial de la VM"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    Créer une VM pour un utilisateur
    
    Exemples:
    
    \b
    python scripts/create_vm.py
    python scripts/create_vm.py --name "Ma VM" --cores 4
    python scripts/create_vm.py -n "VM Test" --os "CentOS 8" --ram 8
    """

    logger.info(
        "Début du processus de création de VM", email=args.email, vm_name=args.name
    )

    # Initialisation du client API et du service
    api = Api(config.DEMO_API_BASE_URL)
    vm_service = VMService(api)

    # Authentification de l'utilisateur
    logger.info("Authentification de l'utilisateur")
    user = vm_service.authenticate_user(
        email=args.email, password=config.DEMO_API_PASSWORD
    )

    if not user:
        logger.error("Authentification échouée")
        print("❌ Échec de l'authentification")
        sys.exit(1)

    logger.info("Authentification réussie", user_id=user.get("id"))
    print(f"✅ Utilisateur authentifié: {user.get('name', args.email)}")

    # Configuration de la VM
    vm_config = {
        "user_id": user["id"],
        "name": args.name,
        "operating_system": args.os,
        "cpu_cores": args.cores,
        "ram_gb": args.ram,
        "disk_gb": args.disk,
        "status": args.status,
    }

    # Création de la VM
    logger.info("Création de la VM", **vm_config)
    vm_result = vm_service.create_vm_for_user(user, vm_config)

    if vm_result:
        logger.info("VM créée avec succès", vm_id=vm_result.get("id"))
        print(f"✅ VM créée avec succès!")
        print(f"   🆔 ID: {vm_result.get('id')}")
        print(f"   📝 Nom: {vm_result.get('name')}")
        print(f"   💻 OS: {vm_result.get('operating_system')}")
        print(f"   🔧 CPU: {vm_result.get('cpu_cores')} cores")
        print(f"   💾 RAM: {vm_result.get('ram_gb')} GB")
        print(f"   💿 Disque: {vm_result.get('disk_gb')} GB")
        print(f"   ⚡ Statut: {vm_result.get('status')}")
    else:
        logger.error("Échec de la création de la VM")
        print("❌ Échec de la création de la VM")
        sys.exit(1)


if __name__ == "__main__":
    main()
