#!/usr/bin/env python3
"""
Point d'entrée principal pour demo_api

Interface moderne avec Typer pour le management des utilisateurs et VMs.
"""

import sys
import typer
from pathlib import Path
from enum import Enum
from typing import Optional

from utils.api import Api
from utils.services import ReportService, VMService
from utils.logging_config import get_logger
from utils.config import config

logger = get_logger(__name__)
app = typer.Typer(
    name="demo-api",
    help="🏗️ Interface CLI pour demo_api - Management des utilisateurs et VMs",
    rich_markup_mode="markdown",
)


class ReportType(str, Enum):
    """Types de rapport disponibles"""

    USERS_VMS = "users-vms"
    STATUS = "status"
    ALL = "all"


@app.command()
def report(
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
    python main.py report
    python main.py report --type users-vms
    python main.py report -t status -o ./rapports --verbose
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
            logger.error("Échec de la génération du rapport utilisateurs/VMs")
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


@app.command()
def create(
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
    python main.py create
    python main.py create --name "Ma VM" --cores 4
    python main.py create -n "VM Test" --ram 8 --disk 100 --verbose
    """

    # Configurer le nom par défaut si non fourni
    vm_name = name or "VM de Jean"

    if verbose:
        print(f"🔧 Configuration VM:")
        print(f"   Nom: {vm_name}")
        print(f"   OS: {os}")
        print(f"   CPU: {cores} cores")
        print(f"   RAM: {ram} GB")
        print(f"   Disque: {disk} GB")
        print(f"   Statut: {status}")
        print(f"   Email: {email}")
        print()

    logger.info("Début du processus de création de VM", email=email, vm_name=vm_name)

    # Initialisation du client API et du service
    api = Api(config.DEMO_API_BASE_URL)
    vm_service = VMService(api)

    # Authentification de l'utilisateur
    typer.echo("🔐 Authentification de l'utilisateur...")
    logger.info("Authentification de l'utilisateur")
    user = vm_service.authenticate_user(email=email, password=config.DEMO_API_PASSWORD)

    if not user:
        logger.error("Authentification échouée")
        typer.echo("❌ Échec de l'authentification")
        raise typer.Exit(1)

    logger.info("Authentification réussie", user_id=user.get("id"))
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
        print(f"🚀 Création de la VM...")

    # Création de la VM
    logger.info("Création de la VM", **vm_config)
    vm_result = vm_service.create_vm_for_user(user, vm_config)

    print()
    if vm_result:
        logger.info("VM créée avec succès", vm_id=vm_result.get("id"))
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
        logger.error("Échec de la création de la VM")
        typer.echo("❌ Échec de la création de la VM")
        raise typer.Exit(1)


@app.command()
def version() -> None:
    """📋 Afficher la version"""
    typer.echo("demo-api CLI v3.0.0")
    typer.echo("Powered by Typer 🚀")


def main():
    """Point d'entrée principal"""
    try:
        app()
    except KeyboardInterrupt:
        logger.info("Exécution interrompue par l'utilisateur")
        typer.echo("\n⚠️  Exécution interrompue")
    except Exception as e:
        logger.error("Erreur lors de l'exécution", error=str(e))
        typer.echo(f"❌ Erreur: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
