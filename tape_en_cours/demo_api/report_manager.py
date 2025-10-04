#!/usr/bin/env python3
"""
Gestionnaire de rapports pour demo_api
"""

import typer
from enum import Enum
from typing import Dict, Any, List, Optional
from utils.api import Api
from utils.api.exceptions import UsersFetchError, VMsFetchError
from utils.logging_config import get_logger
from utils.config import config
from reports import JSONReportGenerator

logger = get_logger(__name__)


class ReportType(str, Enum):
    """Types de rapport disponibles"""

    USERS_VMS = "users-vms"
    STATUS = "status"
    ALL = "all"


def fetch_report_data(api: Api) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Récupère les données des utilisateurs et VMs depuis l'API

    Returns:
        Tuple contenant (users, vms) ou ([], []) en cas d'erreur
    """
    logger.info("Début de récupération des données pour rapport")

    # Récupération des utilisateurs
    try:
        users = api.users.get()
        logger.info("Utilisateurs récupérés", count=len(users))
    except UsersFetchError as e:
        logger.error("Impossible de récupérer les utilisateurs", error=str(e))
        users = []

    # Récupération des VMs
    try:
        vms = api.vms.get()
        logger.info("VMs récupérées", count=len(vms))
    except VMsFetchError as e:
        logger.error("Impossible de récupérer les VMs", error=str(e))
        vms = []

    return users, vms


def generate_users_vms_report(api: Api, filename: str = "vm_users.json") -> Optional[str]:
    """
    Génère un rapport utilisateurs/VMs

    Args:
        api: Client API unifié
        filename: Nom du fichier de sortie

    Returns:
        Chemin du fichier généré ou None si échec
    """
    logger.info("Début de génération du rapport utilisateurs/VMs")

    # Récupérer les données
    users, vms = fetch_report_data(api)

    if not users or not vms:
        logger.warning(
            "Impossible de générer le rapport: données manquantes",
            users_count=len(users),
            vms_count=len(vms),
        )
        return None

    # Associer les VMs aux utilisateurs
    api.users.add_vms_to_users(users, vms)

    # Génération du rapport JSON
    try:
        logger.info("Génération du rapport JSON")
        json_generator = JSONReportGenerator()
        report_file = json_generator.generate_users_vms_report(users, filename)
        logger.info("Rapport JSON généré avec succès", filename=report_file)
        return report_file
    except (IOError, TypeError) as e:
        logger.error("Erreur lors de la génération du rapport", error=str(e))
        return None


def generate_status_report(api: Api, filename: str = "vm_status_report.json") -> Optional[str]:
    """
    Génère un rapport des VMs par statut

    Args:
        api: Client API unifié
        filename: Nom du fichier de sortie

    Returns:
        Chemin du fichier généré ou None si échec
    """
    logger.info("Début de génération du rapport de statut des VMs")

    # Récupérer les données
    users, vms = fetch_report_data(api)

    if not vms:
        logger.warning(
            "Impossible de générer le rapport de statut: pas de VMs disponibles"
        )
        return None

    # Compter les VMs par statut
    status_counts = {}
    for vm in vms:
        status = vm.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1

    # Créer le rapport
    status_report = {
        "metadata": {
            "generated_at": "now",  # Le générateur ajoutera le timestamp
            "total_vms": len(vms),
            "total_users": len(users),
        },
        "vm_status_summary": status_counts,
    }

    try:
        json_generator = JSONReportGenerator()
        report_file = json_generator.generate(status_report, filename)
        logger.info("Rapport de statut généré avec succès", filename=report_file)
        return report_file
    except (IOError, TypeError) as e:
        logger.error(
            "Erreur lors de la génération du rapport de statut", error=str(e)
        )
        return None


def generate_reports(
    report_type: ReportType = typer.Option(
        ReportType.ALL, "--type", "-t", help="Type de rapport à générer"
    ),
    output_dir: str = typer.Option(
        "outputs", "--output-dir", "-o", help="Répertoire de sortie pour les rapports"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    📊 Générer des rapports

    Exemples:

    \b
    python report_manager.py
    python report_manager.py --type users-vms
    python report_manager.py -t status -o ./rapports --verbose
    """

    if verbose:
        typer.echo("🔧 Configuration:")
        typer.echo(f"   Type de rapport: {report_type.value}")
        typer.echo(f"   Répertoire de sortie: {output_dir}")
        typer.echo()

    logger.info(
        "Début de génération des rapports",
        report_type=report_type.value,
        output_dir=output_dir,
    )

    # Initialisation du client API
    api = Api(config.DEMO_API_BASE_URL)

    # Génération des rapports selon le type demandé
    generated_files = []

    if report_type in [ReportType.USERS_VMS, ReportType.ALL]:
        typer.echo("📊 Génération du rapport utilisateurs/VMs...")

        report_file = generate_users_vms_report(api, "vm_users.json")
        if report_file:
            generated_files.append(report_file)
            if verbose:
                typer.echo(f"   ✅ Généré: {report_file}")
        else:
            typer.echo("❌ Échec de la génération du rapport utilisateurs/VMs")

    if report_type in [ReportType.STATUS, ReportType.ALL]:
        typer.echo("📈 Génération du rapport de statut des VMs...")

        status_file = generate_status_report(api, "vm_status_report.json")
        if status_file:
            generated_files.append(status_file)
            if verbose:
                typer.echo(f"   ✅ Généré: {status_file}")
        else:
            typer.echo("❌ Échec de la génération du rapport de statut")

    # Résumé
    typer.echo()
    if generated_files:
        typer.echo(f"🎉 {len(generated_files)} rapport(s) généré(s) avec succès")
        for file in generated_files:
            typer.echo(f"   📄 {file}")
        typer.echo()
        typer.echo("✨ Génération terminée!")
    else:
        typer.echo("❌ Aucun rapport n'a pu être généré")
        raise typer.Exit(1)


if __name__ == "__main__":
    app = typer.Typer(help="Générer les rapports de l'API demo")
    app.command()(generate_reports)
    app()
