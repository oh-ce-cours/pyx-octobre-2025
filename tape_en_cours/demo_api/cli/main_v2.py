#!/usr/bin/env python3
"""
Interface CLI principale avec Typer pour demo_api

Usage:
    python cli/main_v2.py report --help
    python cli/main_v2.py vm create --help
    python cli/main_v2.py --help
"""

import sys
import typer
from pathlib import Path
from enum import Enum
from typing import Optional

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logging_config import get_logger

logger = get_logger("cli")

# Créer l'app principale
app = typer.Typer(
    name="demo-api",
    help="🏗️ Interface CLI pour demo_api - Management des utilisateurs et VMs",
    add_completion=False,
    rich_markup_mode="markdown"
)


class ReportType(str, Enum):
    """Types de rapport disponibles"""
    USERS_VMS = "users-vms"
    STATUS = "status"
    ALL = "all"


def version_callback(value: bool):
    """Affiche la version"""
    if value:
        typer.echo("demo-api CLI v2.0.0")
        raise typer.Exit()


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
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Mode verbeux"
] ):
    """
    📊 Générer des rapports
    
    Exemples:
    
    \b
    python cli/main_v2.py report
    python cli/main_v2.py report --type users-vms
    python cli/main_v2.py report -t status -o ./rapports
    """
    typer.echo(f"🚀 Génération du rapport: {report_type.value}")
    
    # Réexécuter le script avec les bons arguments
    import subprocess
    
    cmd = [
        sys.executable, 
        str(Path(__file__).parent.parent / "scripts" / "generate_report_v2.py"),
        "--report-type", report_type.value,
        "--output-dir", output_dir
    ]
    
    if verbose:
        cmd.append("--verbose")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        typer.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error("Erreur lors de l'exécution du script de rapport", error=e.stderr)
        typer.echo(e.stderr)
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
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Mode verbeux"
    )
) -> None:
    """
    🖥️ Créer une VM
    
    Exemples:
    
    \b
    python cli/main_v2.py vm
    python cli/main_v2.py vm --name "Ma VM" --cores 4
    python cli/main_v2.py vm -n "VM Test" --ram 8 --disk 100
    """
    typer.echo("☁️ Création de VM")
    
    # Configurer le nom par défaut si non fourni
    name = create_name or "VM de Jean"
    
    # Réexécuter le script avec les bons arguments
    import subprocess
    
    cmd = [
        sys.executable,
        str(Path(__file__).parent.parent / "scripts" / "create_vm_v2.py"),
        "--email", email,
        "--name", name,
        "--os", os,
        "--cores", str(cores),
        "--ram", str(ram),
        "--disk", str(disk),
        "--status", status
    ]
    
    if verbose:
        cmd.append("--verbose")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        typer.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error("Erreur lors de l'exécution du script de création VM", error=e.stderr)
        typer.echo(e.stderr)
        raise typer.Exit(1)


# Commande de test/debug
@app.command()
def version() -> None:
    """📋 Afficher la version"""
    typer.echo("demo-api CLI v2.0.0")
    typer.echo("Powered by Typer 🚀")


if __name__ == "__main__":
    app()
