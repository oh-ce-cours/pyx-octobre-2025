#!/usr/bin/env python3
"""
Gestionnaire de rapports pour demo_api
"""

import typer
from enum import Enum
from utils.api import Api
from utils.services import ReportService, DataManager
from utils.logging_config import get_logger
from utils.config import config

logger = get_logger(__name__)


class ReportType(str, Enum):
    """Types de rapport disponibles"""

    USERS_VMS = "users-vms"
    STATUS = "status"
    ALL = "all"


class ReportFormat(str, Enum):
    """Formats de rapport disponibles"""

    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"
    ALL = "all"


def generate_reports(
    report_type: ReportType = typer.Option(
        ReportType.ALL, "--type", "-t", help="Type de rapport à générer"
    ),
    report_format: ReportFormat = typer.Option(
        ReportFormat.ALL,
        "--format",
        "-f",
        help="Format de rapport (json, markdown, html, all)",
    ),
    output_dir: str = typer.Option(
        "outputs", "--output-dir", "-o", help="Répertoire de sortie pour les rapports"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    📊 Générer des rapports

    Exemples:

    .. code-block:: shell

        python report_manager.py
        python report_manager.py --type users-vms --format markdown
        python report_manager.py -t status -f html -o ./rapports --verbose
        python report_manager.py --format all --type all
    """

    if verbose:
        typer.echo("🔧 Configuration:")
        typer.echo(f"   Type de rapport: {report_type.value}")
        typer.echo(f"   Format: {report_format.value}")
        typer.echo(f"   Répertoire de sortie: {output_dir}")
        typer.echo()

    logger.info(
        "Début de génération des rapports",
        report_type=report_type.value,
        format=report_format.value,
        output_dir=output_dir,
    )

    # Initialisation du client API, du gestionnaire de données et du service
    api = Api(config.DEMO_API_BASE_URL)
    data_manager = DataManager(api)
    report_service = ReportService(api)

    # Récupération centralisée des données (une seule fois)
    typer.echo("📡 Récupération des données...")
    users, vms = data_manager.fetch_all_data()

    if not users and not vms:
        typer.echo("❌ Impossible de récupérer les données nécessaires")
        raise typer.Exit(1)

    typer.echo(f"   ✅ {len(users)} utilisateur(s) et {len(vms)} VM(s) récupéré(s)")
    typer.echo()

    # Génération des rapports selon le type et format demandés
    generated_files = []

    # Déterminer les formats à générer
    formats_to_generate = []
    if report_format == ReportFormat.ALL:
        formats_to_generate = [
            ReportFormat.JSON,
            ReportFormat.MARKDOWN,
            ReportFormat.HTML,
        ]
    else:
        formats_to_generate = [report_format]

    # Génération des rapports utilisateurs/VMs
    if report_type in [ReportType.USERS_VMS, ReportType.ALL]:
        typer.echo("📊 Génération du rapport utilisateurs/VMs...")

        for fmt in formats_to_generate:
            report_file = None
            if fmt == ReportFormat.JSON:
                report_file = report_service.generate_users_vms_report(
                    users, vms, "vm_users.json"
                )
            elif fmt == ReportFormat.MARKDOWN:
                report_file = report_service.generate_users_vms_report_markdown(
                    users, vms, "vm_users.md"
                )
            elif fmt == ReportFormat.HTML:
                report_file = report_service.generate_users_vms_report_html(
                    users, vms, "vm_users.html"
                )

            if report_file:
                generated_files.append(report_file)
                if verbose:
                    typer.echo(f"   ✅ Généré ({fmt.value}): {report_file}")
            else:
                typer.echo(
                    f"❌ Échec de la génération du rapport utilisateurs/VMs ({fmt.value})"
                )

    # Génération des rapports de statut
    if report_type in [ReportType.STATUS, ReportType.ALL]:
        typer.echo("📈 Génération du rapport de statut des VMs...")

        for fmt in formats_to_generate:
            status_file = None
            if fmt == ReportFormat.JSON:
                status_file = report_service.generate_status_report(
                    users, vms, "vm_status_report.json"
                )
            elif fmt == ReportFormat.MARKDOWN:
                status_file = report_service.generate_status_report_markdown(
                    users, vms, "vm_status_report.md"
                )
            elif fmt == ReportFormat.HTML:
                status_file = report_service.generate_status_report_html(
                    users, vms, "vm_status_report.html"
                )

            if status_file:
                generated_files.append(status_file)
                if verbose:
                    typer.echo(f"   ✅ Généré ({fmt.value}): {status_file}")
            else:
                typer.echo(
                    f"❌ Échec de la génération du rapport de statut ({fmt.value})"
                )

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
