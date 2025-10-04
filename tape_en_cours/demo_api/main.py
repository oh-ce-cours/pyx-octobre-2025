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
def signup(
    name: str = typer.Option("Jean Dupont", "--name", "-n", help="Nom de l'utilisateur"),
    email: str = typer.Option(
        "jean@dupont21.com", "--email", "-e", help="Email de l'utilisateur"
    ),
    password: str = typer.Option(
        "password123", "--password", "-p", help="Mot de passe de l'utilisateur"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    👤 Créer un nouvel utilisateur avec authentification

    Crée un utilisateur via /auth/signup et récupère son token d'authentification.

    Exemples:

    \b
    python main.py signup
    python main.py signup --name "Alice Martin" --email "alice@example.com"
    python main.py signup -n "Bob Dupont" -e "bob@test.com" -p "monmotdepasse" --verbose
    """
    from utils.api.auth import Auth
    from utils.config import config
    
    if verbose:
        typer.echo("🔧 Configuration utilisateur:")
        typer.echo(f"   Nom: {name}")
        typer.echo(f"   Email: {email}")
        typer.echo(f"   Mot de passe: {'*' * len(password)}")
        typer.echo()

    logger.info("Début du processus de création d'utilisateur", email=email, name=name)

    # Initialisation du client Auth
    auth = Auth(config.DEMO_API_BASE_URL)
    
    try:
        # Création de l'utilisateur via /auth/signup
        typer.echo("🔐 Création de l'utilisateur...")
        token = auth.create_user(name=name, email=email, password=password)
        
        if token:
            typer.echo("✅ Utilisateur créé avec succès!")
            typer.echo(f"   👤 Nom: {name}")
            typer.echo(f"   📧 Email: {email}")
            typer.echo(f"   🔑 Token: {token[:20]}...")
            typer.echo()
            
            # Récupérer les informations complètes de l'utilisateur
            typer.echo("📋 Récupération des informations utilisateur...")
            user_info = auth.get_logged_user_info(token)
            
            if user_info:
                typer.echo("✅ Informations utilisateur récupérées:")
                typer.echo(f"   🆔 ID: {user_info.get('id')}")
                typer.echo(f"   👤 Nom: {user_info.get('name')}")
                typer.echo(f"   📧 Email: {user_info.get('email')}")
                typer.echo(f"   📅 Créé le: {user_info.get('created_at', 'N/A')}")
                typer.echo()
                typer.echo("✨ Utilisateur prêt à utiliser!")
            else:
                typer.echo("⚠️ Utilisateur créé mais impossible de récupérer les informations")
        else:
            typer.echo("❌ Échec de la création de l'utilisateur")
            raise typer.Exit(1)
            
    except Exception as e:
        logger.error("Erreur lors de la création de l'utilisateur", error=str(e))
        typer.echo(f"❌ Erreur lors de la création: {e}")
        raise typer.Exit(1)


@app.command()
def create(
    name: str = typer.Option("VM de Jean", "--name", "-n", help="Nom de la VM"),
    email: str = typer.Option(
        "jean@dupont21.com", "--email", "-e", help="Email de l'utilisateur existant"
    ),
    password: str = typer.Option(
        "password123", "--password", "-p", help="Mot de passe de l'utilisateur"
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
    🖥️ Créer une VM pour un utilisateur existant

    Authentifie un utilisateur existant et crée une VM pour lui.

    Exemples:

    \b
    python main.py create
    python main.py create --name "Ma VM" --email "alice@example.com" --password "motdepasse"
    python main.py create -n "VM Test" --ram 8 --disk 100 --verbose
    """
    # Appeler directement la fonction avec le mot de passe
    create_vm(name, email, password, os, cores, ram, disk, status, verbose)


@app.command()
def generate(
    user_count: int = typer.Option(
        50, "--users", "-u", help="Nombre d'utilisateurs à générer", min=1, max=1000
    ),
    min_vms: int = typer.Option(
        0, "--min-vms", help="Nombre minimum de VMs par utilisateur", min=0, max=10
    ),
    max_vms: int = typer.Option(
        5, "--max-vms", help="Nombre maximum de VMs par utilisateur", min=0, max=20
    ),
    output_file: str = typer.Option(
        "vm_users.json", "--output", "-o", help="Fichier de sortie JSON"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    🎲 Générer des données factices avec Faker

    Génère un dataset complet d'utilisateurs français avec des VMs réalistes.
    Les données sont sauvegardées dans un fichier JSON.

    Exemples:

    \b
    python main.py generate
    python main.py generate --users 100 --max-vms 3
    python main.py generate -u 25 -o mon_dataset.json --verbose
    """
    if min_vms > max_vms:
        typer.echo("❌ Le nombre minimum de VMs ne peut pas être supérieur au maximum")
        raise typer.Exit(1)

    typer.echo(
        f"🎲 Génération de {user_count} utilisateurs avec {min_vms}-{max_vms} VMs chacun..."
    )

    try:
        # Générer les données
        users_data = DataGenerator.generate_users_with_vms(
            user_count=user_count, vm_per_user_range=(min_vms, max_vms)
        )

        # Sauvegarder dans le fichier JSON
        output_path = Path(output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(users_data, f, indent=4, ensure_ascii=False, default=str)

        # Statistiques
        total_vms = sum(len(user["vms"]) for user in users_data)
        users_with_vms_count = len([u for u in users_data if u["vms"]])

        typer.echo("✅ Données générées avec succès !")
        typer.echo("📊 Statistiques:")
        typer.echo(f"   • Utilisateurs: {len(users_data)}")
        typer.echo(f"   • VMs totales: {total_vms}")
        typer.echo(f"   • Utilisateurs avec VMs: {users_with_vms_count}")
        typer.echo(f"   • Moyenne VMs/utilisateur: {total_vms / len(users_data):.1f}")
        typer.echo(f"📁 Fichier sauvegardé: {output_path.absolute()}")

        if verbose:
            typer.echo("\n🔍 Aperçu des données générées:")
            for i, user in enumerate(users_data[:3]):
                typer.echo(
                    f"   {i + 1}. {user['name']} ({user['email']}) - {len(user['vms'])} VMs"
                )
            if len(users_data) > 3:
                typer.echo(f"   ... et {len(users_data) - 3} autres utilisateurs")

    except Exception as e:
        logger.error("Erreur lors de la génération des données", error=str(e))
        typer.echo(f"❌ Erreur lors de la génération: {e}")
        raise typer.Exit(1)


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
