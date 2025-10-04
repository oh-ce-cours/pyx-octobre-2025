#!/usr/bin/env python3
"""
Script de génération de rapports

Ce script génère les rapports disponibles :
- Rapport utilisateurs/VMs
- Rapport de statut des VMs
"""

import sys
import argparse
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.api import Api
from utils.services import ReportService
from utils.logging_config import get_logger
from utils.config import config

logger = get_logger("generate_report")


def main():
    """Point d'entrée principal du script de génération de rapports"""

    parser = argparse.ArgumentParser(description="Générer les rapports de l'API demo")
    parser.add_argument(
        "--report-type",
        choices=["users-vms", "status", "all"],
        default="all",
        help="Type de rapport à générer (défaut: all)",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Répertoire de sortie pour les rapports (défaut: outputs)",
    )

    args = parser.parse_args()

    logger.info(
        "Début de génération des rapports",
        report_type=args.report_type,
        output_dir=args.output_dir,
    )

    # Initialisation du client API et du service
    api = Api(config.DEMO_API_BASE_URL)
    report_service = ReportService(api)

    # Génération des rapports selon le type demandé
    generated_files = []

    if args.report_type in ["users-vms", "all"]:
        logger.info("Génération du rapport utilisateurs/VMs")
        report_file = report_service.generate_users_vms_report("vm_users.json")
        if report_file:
            generated_files.append(report_file)
        else:
            logger.error("Échec de la génération du rapport utilisateurs/VMs")

    if args.report_type in ["status", "all"]:
        logger.info("Génération du rapport de statut des VMs")
        status_file = report_service.generate_status_report("vm_status_report.json")
        if status_file:
            generated_files.append(status_file)
        else:
            logger.error("Échec de la génération du rapport de statut")

    # Résumé
    if generated_files:
        logger.info(
            "Génération terminée avec succès",
            files_generated=len(generated_files),
            files=generated_files,
        )
        print(f"✅ {len(generated_files)} rapport(s) généré(s) avec succès")
        for file in generated_files:
            print(f"   📄 {file}")
    else:
        logger.error("Aucun rapport n'a pu être généré")
        print("❌ Aucun rapport n'a pu être généré")
        sys.exit(1)


if __name__ == "__main__":
    main()
