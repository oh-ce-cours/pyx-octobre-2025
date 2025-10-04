#!/usr/bin/env python3
"""
Point d'entrée principal avec Typer pour demo_api

Ce fichier sert maintenant de point d'entrée unifié avec Typer
"""

import sys
import typer
from pathlib import Path
from enum import Enum
from typing import Optional

# Imports pour la compatibilité avec l'ancien comportement
from utils.api import Api
from utils.services import ReportService, VMService
from utils.logging_config import get_logger
from utils.config import config

logger = get_logger(__name__)
app = typer.Typer(
    name="demo-api",
    help="🏗️ Interface CLI pour demo_api - Management des utilisateurs et VMs",
    rich_markup_mode="markdown"
)


class ReportType(str, Enum):
    """Types de rapport disponibles"""
    USERS_VMS = "users-vms"
    STATUS = "status"
    ALL = "all"


def legacy_report_generation():
    """Exécute la génération de rapports selon l'ancien comportement"""
    logger.info("Exécution en mode legacy: génération de rapport")
    
    api = Api(config.DEMO_API_BASE_URL)
    report_service = ReportService(api)
    report_file = report_service.generate_users_vms_report("vm_users.json")
    
    if report_file:
        typer.echo(f"✅ Rapport généré: {report_file}")
    else:
        typer.echo("❌ Échec de la génération du rapport")


def legacy_vm_creation():
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
        typer.echo(f"✅ Utilisateur authentifié: {user.get('name')}")
        vm_result = vm_service.create_default_vm_for_user(user)
        
        if vm_result:
            typer.echo(f"✅ VM créée: {vm_result.get('name')} (ID: {vm_result.get('id')})")
        else:
            typer.echo("❌ Échec de la création de la VM")
    else:
        typer.echo("❌ Échec de l'authentification")


@app.command()
def report(
    report_type: ReportType = typer.Option(
        ReportType.ALL,
        "--type",
        "-t",
        help="Type de rapport à générer"
    ),
    output_dir: str = typer.Option(
        "outputs",
        "--output-dir",
        "-o",
        help="Répertoire de sortie pour les rapports"
    ),
    legacy_mode: bool = typer.Option(
        False,
        "--legacy",
        help="Mode legacy (compatibilité avec ancien comportement)"
    )
) -> None:
    """
    📊 Générer des rapports

    Exemples:

    \b
    python main_v2.py report
    python main_v2.py report --type users-vms
    python main_v2.py report -t status -o ./rapports
    """
    if legacy_mode:
        typer.echo("Mode legacy activé")
        legacy_report_generation()
        return
    
    typer.echo(f"🚀 Génération du rapport: {report_type.value}")
    
    # Exécuter le script de génération de rapport
    import subprocess
    
    cmd = [
        sys.executable, 
        str(Path(__file__).parent / "scripts" / "generate_report.py"),
        "--report-type", report_type.value,
        "--output-dir", output_dir,
        "--verbose"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        typer.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error("Erreur lors de l'exécution du script de rapport", error=e.stderr)
        typer.echo(e.stderr or "")
        raise typer.Exit(1)


@app.command()
def vm(
    create_name: Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="Nom de la VM"
    ),
    email: str = typer.Option(
        "jean@dupont21.com",
        "--email",
        "-e",
        help="Email de l'utilisateur"
    ),
    os: str = typer.Option(
        "Ubuntu 22.04",
        "--os",
        help="Système d'exploitation"
    ),
    cores: int = typer.Option(
        2,
        "--cores",
        "-c",
        help="Nombre de cœurs CPU",
        min=1,
        max=16
    ),
    ram: int = typer.Option(
        4,
        "--ram",
        "-r",
        help="RAM en GB",
        min=1,
        max=128
    ),
    disk: int = typer.Option(
        50,
        "--disk",
        "-d",
        help="Disque en GB",
        min=10,
        max=2048
    ),
    status: str = typer.Option(
        "stopped",
        "--status",
        "-s",
        help="Statut initial de la VM"
    ),
    legacy_mode: bool = typer.Option(
        False,
        "--legacy",
        help="Mode legacy (compatibilité avec ancien comportement)"
    )
) -> None:
    """
    🖥️ Créer une VM

    Exemples:

    \b
    python main_v2.py vm
    python main_v2.py vm --name "Ma VM" --cores 4
    python main_v2.py vm -n "VM Test" --ram 8 --disk 100
    """
    if legacy_mode:
        typer.echo("Mode legacy activé")
        legacy_vm_creation()
        return
    
    typer.echo("☁️ Création de VM")
    
    # Configurer le nom par défaut si non fourni
    name = create_name or "VM de Jean"
    
    # Exécuter le script de création VM
    import subprocess
    
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "scripts" / "create_vm.py"),
        "--email", email,
        "--name", name,
        "--os", os,
        "--cores", str(cores),
        "--ram", str(ram),
        "--disk", str(disk),
        "--status", status,
        "--verbose"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        typer.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error("Erreur lors de l'exécution du script de création VM", error=e.stderr else "")
        typer.echo(e.stderr or "")
        raise typer.Exit(1)


@app.command()
def legacy() -> None:
    """🔄 Exécuter les deux opérations principales comme dans l'ancien comportement"""
    logger.info("Exécution en mode legacy complet")
    
    typer.echo("🚀 Démarrage de demo_api en mode legacy")
    typer.echo("-" * 50)
    
    typer.echo("\n📊 Génération de rapport...")
    legacy_report_generation()
    
    typer.echo("\n🖥️  Création de VM...")
    legacy_vm_creation()
    
    typer.echo("\n✅ Exécution terminée")


@app.command()
def version() -> None:
    """📋 Afficher la version"""
    typer.echo("demo-api CLI v3.0.0")
    typer.echo("Powered by Typer 🚀")


if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        logger.info("Exécution interrompue par l'utilisateur")
        typer.echo("\n⚠️  Exécution interrompue")
    except Exception as e:
        logger.error("Erreur lors de l'exécution", error=str(e))
        typer.echo(f"❌ Erreur: {e}")
        sys.exit(1)
