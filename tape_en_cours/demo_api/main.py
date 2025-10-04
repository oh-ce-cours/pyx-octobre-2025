#!/usr/bin/env python3
"""
Point d'entrée principal pour demo_api

Interface d'orchestration avec Typer pour le management des utilisateurs et VMs.
"""

import typer
from utils.logging_config import get_logger
from report_manager import generate_reports, ReportType, ReportFormat
from vm_manager import create_vm
from utils.data_generator import DataGenerator
import json
from pathlib import Path

logger = get_logger(__name__)

app = typer.Typer(
    name="demo-api",
    help="🏗️ Interface CLI pour demo_api - Management des utilisateurs et VMs",
    rich_markup_mode="markdown",
    add_completion=False,
    no_args_is_help=True,
)


@app.command()
def report(
    report_type: str = typer.Option(
        "all", "--type", "-t", help="Type de rapport à générer (all, users-vms, status)"
    ),
    report_format: str = typer.Option(
        "all", "--format", "-f", help="Format de rapport (all, json, markdown, html)"
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
    python main.py report --type users-vms --format markdown
    python main.py report -t status -f html -o ./rapports --verbose
    python main.py report --format all --type all
    """
    # Convertir les strings en enums
    try:
        report_type_enum = ReportType(report_type)
    except ValueError as exc:
        typer.echo(f"❌ Type de rapport invalide: {report_type}")
        typer.echo("Types valides: all, users-vms, status")
        raise typer.Exit(1) from exc

    try:
        format_enum = ReportFormat(report_format)
    except ValueError as exc:
        typer.echo(f"❌ Format de rapport invalide: {report_format}")
        typer.echo("Formats valides: all, json, markdown, html")
        raise typer.Exit(1) from exc

    # Appeler directement la fonction
    generate_reports(report_type_enum, format_enum, output_dir, verbose)


@app.command()
def create(
    name: str = typer.Option("VM de Jean", "--name", "-n", help="Nom de la VM"),
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
    # Appeler directement la fonction
    create_vm(name, email, os, cores, ram, disk, status, verbose)


@app.command()
def version() -> None:
    """📋 Afficher la version"""
    typer.echo("demo-api CLI v3.0.0")
    typer.echo("Powered by Typer 🚀")


def main():
    """Point d'entrée principal"""
    import sys

    # Gérer -h comme alias pour --help
    if "-h" in sys.argv and "--help" not in sys.argv:
        sys.argv[sys.argv.index("-h")] = "--help"

    try:
        app()
    except KeyboardInterrupt:
        typer.echo("\n⚠️  Exécution interrompue")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    main()
