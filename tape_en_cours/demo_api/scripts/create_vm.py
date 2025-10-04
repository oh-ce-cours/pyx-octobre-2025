#!/usr/bin/env python3
"""
Script de création de VM

Ce script authentifie un utilisateur et crée une VM selon la configuration spécifiée.
"""

import sys
import argparse
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.api import Api
from utils.services import VMService
from utils.logging_config import get_logger
from utils.config import config

logger = get_logger("create_vm")


def main():
    """Point d'entrée principal du script de création de VM"""
    
    parser = argparse.ArgumentParser(
        description="Créer une VM pour un utilisateur"
    )
    parser.add_argument(
        "--email",
        default="jean@dupont21.com",
        help="Email de l'utilisateur (défaut: jean@dupont21.com)"
    )
    parser.add_argument(
        "--name",
        default="VM de Jean",
        help="Nom de la VM (défaut: VM de Jean)"
    )
    parser.add_argument(
        "--os",
        default="Ubuntu 22.04",
        help="Système d'exploitation (défaut: Ubunto 22.04)"
    )
    parser.add_argument(
        "--cores",
        type=int,
        default=2,
        help="Nombre de cœurs CPU (défaut: 2)"
    )
    parser.add_argument(
        "--ram",
        type=int,
        default=4,
        help="RAM en GB (défaut: 4)"
    )
    parser.add_argument(
        "--disk",
        type=int,
        default=50,
        help="Disque en GB (défaut: 50)"
    )
    parser.add_argument(
        "--status",
        default="stopped",
        help="Statut initial de la VM (défaut: stopped)"
    )
    
    args = parser.parse_args()
    
    logger.info("Début du processus de création de VM", 
                email=args.email,
                vm_name=args.name)
    
    # Initialisation du client API et du service
    api = Api(config.DEMO_API_BASE_URL)
    vm_service = VMService(api)
    
    # Authentification de l'utilisateur
    logger.info("Authentification de l'utilisateur")
    user = vm_service.authenticate_user(email=args.email, password=config.DEMO_API_PASSWORD)
    
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
