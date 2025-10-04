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

from utils.logging_config import get_logger

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
    typer.echo(f"🚀 Génération du rapport: {report_type.value}")

    # Exécuter le script de génération de rapport
    import subprocess

    cmd = [
        sys.executable,
        str(Path(__file__).parent / "scripts" / "generate_report.py"),
        "--report-type",
        report_type.value,
        "--output-dir",
        output_dir,
    ]

    if verbose:
        cmd.append("--verbose")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        typer.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error("Erreur lors de l'exécution du script de rapport", error=e.stderr)
        typer.echo(e.stderr or "")
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
    typer.echo("☁️ Création de VM")

    # Configurer le nom par défaut si non fourni
    vm_name = name or "VM de Jean"

    # Exécuter le script de création VM
    import subprocess

    cmd = [
        sys.executable,
        str(Path(__file__).parent / "scripts" / "create_vm.py"),
        "--email",
        email,
        "--name",
        vm_name,
        "--os",
        os,
        "--cores",
        str(cores),
        "--ram",
        str(ram),
        "--disk",
        str(disk),
        "--status",
        status,
    ]

    if verbose:
        cmd.append("--verbose")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, 文本=True)
        typer.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(
            "Erreur lors de l'exécution du script de création VM", error=e.stderr
        )
        typer.echo(e.stderr or "")
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
