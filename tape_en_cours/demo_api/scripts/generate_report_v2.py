#!/usr/bin/env python3
"""
Script de génération de rapports avec Typer

Ce script génère les rapports disponibles :
- Rapport utilisateurs/VMs
- Rapport de statut des VMs
"""

import sys
import typer
from pathlib import Path
from enum import Enum

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.api import Api
from utils.services import ReportService
from utils.logging_config import get_logger
from utils.config import config

logger = get_logger("generate_report")
app = typer.Typer(help="Générer les rapports de l'API demo")


class ReportType(str, Enum):
    """Types de rapport disponibles"""

    USERS_VMS = "users-vms"
    STATUS = "status"
    ALL = "all"


def generate_reports(
    report_type: ReportType = typer.Option(
        ReportType.ALL, "--report-type", "-t", help="Type de rapport à générer"
    ),
    output_dir: str = typer.Option(
        "outputs", "--output-dir", "-o", help="Répertoire de sortie pour les rapports"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    Générer les rapports de l'API demo

    Exemples:

    \b
    python scripts/generate_report_v2.py
    python scripts/generate_report_v2.py --report-type users-vms
    python scripts/generate_report_v2.py -t all -o ./rapports
    """

    if verbose:
        print(f"🔧 Configuration:")
        print(f"   Type de rapport: {report_type.value}")
        print(f"   Répertoire de sortie: {output_dir}")
        print()

    logger.info(
        "Début de génération des rapports",
        report_type=report_type.value,
        output_dir=output_dir,
    )

    # Initialisation du client API et du service
    api = Api(config.DEMO_API_BASE_URL)
    report_service = ReportService(api)

    # Génération des rapports selon le type demandé
    generated_files = []

    if report_type in [ReportType.USERS_VMS, ReportType.ALL]:
        logger.info("Génération du rapport utilisateurs/VMs")
        typer.echo("📊 Génération du rapport utilisateurs/VMs...")

        report_file = report_service.generate_users_vms_report("vm_users.json")
        if report_file:
            generated_files.append(report_file)
            if verbose:
                typer.echo(f"   ✅ Généré: {report_file}")
        else:
            logger.error("Échec de la génération du rapport utilisadores/VMs")
            typer.echo("❌ Échec de la génération du rapport utilisateurs/VMs")

    if report_type in [ReportType.STATUS, ReportType.ALL]:
        logger.info("Génération du rapport de statut des VMs")
        typer.echo("📈 Génération du rapport de statut des VMs...")

        status_file = report_service.generate_status_report("vm_status_report.json")
        if status_file:
            generated_files.append(status_file)
            if verbose:
                typer.echo(f"   ✅ Généré: {status_file}")
        else:
            logger.error("Échec de la génération du rapport de statut")
            typer.echo("❌ Échec de la génération du rapport de statut")

    # Résumé
    print()
    if generated_files:
        logger.info(
            "Génération terminée avec succès",
            files_generated=len(generated_files),
            files=generated_files,
        )
        typer.echo(f"🎉 {len(generated_files)} rapport(s) généré(s) avec succès")
        for file in generated_files:
            typer.echo(f"   📄 {file}")
        typer.echo()
        typer.echo("✨ Génération terminée!")
    else:
        logger.error("Aucun rapport n'a pu être généré")
        typer.echo("❌ Aucun rapport n'a pu être généré")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
