#!/usr/bin/env python3
"""
Point d'entrée principal pour demo_api

Ce fichier sert maintenant de point d'entrée unifié qui redirige vers la CLI
ou exécute directement les fonctionnalités pour maintenir la compatibilité.
"""

import sys
import argparse
from pathlib import Path

# Imports pour la compatibilité avec l'ancien comportement
from utils.api import Api
from utils.services import ReportService, VMService
from utils.logging_config import get_logger
from utils.config import config

logger = get_logger(__name__)


def run_legacy_report_generation():
    """Exécute la génération de rapports selon l'ancien comportement"""
    logger.info("Exécution en mode legacy: génération de rapport")
    
    api = Api(config.DEMO_API_BASE_URL)
    report_service = ReportService(api)
    report_file = report_service.generate_users_vms_report("vm_users.json")
    
    if report_file:
        print(f"✅ Rapport généré: {report_file}")
    else:
        print("❌ Échec de la génération du rapport")


def run_legacy_vm_creation():
    """Exécute la création de VM selon l'ancien comportement"""
    logger.info("Exécution en mode legacy: création de VM")
    
    api = Api(config.DEMO_API_BASE_URL)
    vm_service = VMService(api)
    
    # Authentification
    user = vm_service.authenticate_user(
        email=config.DEMO_API_EMAIL or "jean@dupont21.com",
        password=config.DEMO_API_PASSWORD
    )
    
    if user:
        print(f"✅ Utilisateur authentifié: {user.get('name')}")
        vm_result = vm_service.create_default_vm_for_user(user)
        
        if vm_result:
            print(f"✅ VM créée: {vm_result.get('name')} (ID: {vm_result.get('id')})")
        else:
            print("❌ Échec de la création de la VM")
    else:
        print("❌ Échec de l'authentification")


def run_legacy_mode():
    """Exécute les deux opérations principales comme dans l'ancien comportement"""
    logger.info("Exécution en mode legacy complet")
    print("🚀 Démarrage de demo_api en mode legacy")
    print("-" * 50)
    
    print("\n📊 Génération de rapport...")
    run_legacy_report_generation()
    
    print("\n🖥️  Création de VM...")
    run_legacy_vm_creation()
    
    print("\n✅ Exécution terminée")


def setup_argument_parser():
    """Configuration du parser d'arguments"""
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="Point d'entrée principal pour demo_api",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py                           # Mode legacy (rapport + création VM)
  python main.py --cli report --report-type all
  python main.py --cli vm create --name "Ma VM"
  python main.py --legacy                  # Forcer le mode legacy
        """
    )
    
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Forcer l'exécution en mode legacy (compatibilité)"
    )
    
    parser.add_argument(
        "--cli",
        dest="cli_command",
        nargs="+",
        help="Exécuter une commande CLI spécifique"
    )
    
    return parser


def main():
    """Point d'entrée principal"""
    
    parser = setup_argument_parser()
    args, unknown_args = parser.parse_known_args()
    
    logger.info("Démarrage de demo_api", legacy_mode=args.legacy, cli_command=args.cli_command)
    
    try:
        if args.legacy or not args.cli_command:
            # Mode legacy : compatibilité avec l'ancien comportement
            run_legacy_mode()
        else:
            # Mode CLI : redirection vers la CLI
            # Préparer les arguments pour la CLI
            cli_args = ["cli/main.py"] + args.cli_command + unknown_args
            
            # Remplacer sys.argv pour la CLI
            original_argv = sys.argv
            sys.argv = cli_args
            
            try:
                # Importer et exécuter la CLI
                sys.path.insert(0, str(Path(__file__).parent / "cli"))
                from cli.main import main as cli_main
                cli_main()
            finally:
                # Restaurer sys.argv original
                sys.argv = original_argv
                
    except KeyboardInterrupt:
        logger.info("Exécution interrompue par l'utilisateur")
        print("\n⚠️  Exécution interrompue")
    except (ImportError, OSError, AttributeError) as e:
        logger.error("Erreur lors de l'exécution", error=str(e))
        print(f"❌ Erreur: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()