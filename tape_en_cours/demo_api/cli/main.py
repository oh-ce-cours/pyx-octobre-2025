#!/usr/bin/env python3
"""
Interface CLI principale pour demo_api

Usage:
    python cli/main.py report [options]      # Générer des rapports
    python cli/main.py vm create [options]   # Créer une VM
    python cli/main.py --help               # Aide générale
"""

import sys
import typer
from enum import Enum
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logging_config import get_logger

logger = get_logger("cli")


def setup_argument_parser():
    """Configure le parser d'arguments CLI principal"""

    parser = argparse.ArgumentParser(
        prog="demo-api",
        description="Interface CLI pour demo_api - Management des utilisateurs et VMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  %(prog)s report --report-type all
  %(prog)s report --report-type users-vms --output-dir ./rapports
  %(prog)s vm create --name "Ma VM" --os "CentOS 8"
  %(prog)s vm create --email user@example.com --cores 4 --ram 8
        """,
    )

    # Sous-commandes
    subparsers = parser.add_subparsers(
        dest="command", help="Commandes disponibles", required=True
    )

    # Commande 'report'
    report_parser = subparsers.add_parser("report", help="Générer des rapports")
    report_parser.add_argument(
        "--report-type",
        choices=["users-vms", "status", "all"],
        default="all",
        help="Type de rapport à générer (défaut: all)",
    )
    report_parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Répertoire de sortie pour les rapports (défaut: outputs)",
    )

    # Commande 'vm' avec sous-commandes
    vm_parser = subparsers.add_parser("vm", help="Opérations sur les VMs")

    vm_subparsers = vm_parser.add_subparsers(
        dest="vm_command", help="Actions sur les VMs", required=True
    )

    # Sous-commande 'vm create'
    create_parser = vm_subparsers.add_parser("create", help="Créer une VM")
    create_parser.add_argument(
        "--email",
        default="jean@dupont21.com",
        help="Email de l'utilisateur (défaut: jean@dupont21.com)",
    )
    create_parser.add_argument(
        "--name", default="VM de Jean", help="Nom de la VM (défaut: VM de Jean)"
    )
    create_parser.add_argument(
        "--os",
        default="Ubuntu 22.04",
        help="Système d'exploitation (défaut: Ubuntu 22.04)",
    )
    create_parser.add_argument(
        "--cores", type=int, default=2, help="Nombre de cœurs CPU (défaut: 2)"
    )
    create_parser.add_argument(
        "--ram", type=int, default=4, help="RAM en GB (défaut: 4)"
    )
    create_parser.add_argument(
        "--disk", type=int, default=50, help="Disque en GB (défaut: 50)"
    )
    create_parser.add_argument(
        "--status", default="stopped", help="Statut initial de la VM (défaut: stopped)"
    )

    return parser


def handle_report_command(args):
    """Gère la commande de génération de rapport"""
    from scripts.generate_report import main as report_main

    logger.info("Exécution de la commande report", report_type=args.report_type)

    # Préparer les arguments pour le script de rapport
    sys.argv = [
        "generate_report.py",
        "--report-type",
        args.report_type,
        "--output-dir",
        args.output_dir,
    ]

    try:
        report_main()
    except (ImportError, OSError, AttributeError) as e:
        logger.error("Erreur lors de l'exécution du rapport", error=str(e))
        print(f"❌ Erreur lors de la génération du rapport: {e}")
        sys.exit(1)


def handle_vm_create_command(args):
    """Gère la commande de création de VM"""
    from scripts.create_vm import main as create_vm_main

    logger.info("Exécution de la commande vm create", vm_name=args.name)

    # Préparer les arguments pour le script de création VM
    sys.argv = [
        "create_vm.py",
        "--email",
        args.email,
        "--name",
        args.name,
        "--os",
        args.os,
        "--cores",
        str(args.cores),
        "--ram",
        str(args.ram),
        "--disk",
        str(args.disk),
        "--status",
        args.status,
    ]

    try:
        create_vm_main()
    except (ImportError, OSError, AttributeError) as e:
        logger.error("Erreur lors de l'exécution de la création VM", error=str(e))
        print(f"❌ Erreur lors de la création de la VM: {e}")
        sys.exit(1)


def main():
    """Point d'entrée principal de la CLI"""

    parser = setup_argument_parser()
    args = parser.parse_args()

    logger.info("Début de l'exécution CLI", command=args.command)

    if args.command == "report":
        handle_report_command(args)
    elif args.command == "vm" and args.vm_command == "create":
        handle_vm_create_command(args)
    else:
        logger.error(
            "Commande inconnue",
            command=args.command,
            vm_command=getattr(args, "vm_command", None),
        )
        print(f"❌ Commande inconnue: {args.command}")
        sys.exit(1)

    logger.info("Exécution CLI terminée avec succès")


if __name__ == "__main__":
    main()
