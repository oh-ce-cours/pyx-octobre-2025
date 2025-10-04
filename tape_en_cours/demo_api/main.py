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
from api_data_manager import APIIntegrationService
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

        typer.echo(f"✅ Données générées avec succès !")
        typer.echo(f"📊 Statistiques:")
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
def api_generate(
    base_url: str = typer.Option(
        ..., "--base-url", "-u", help="URL de base de l'API"
    ),
    user_count: int = typer.Option(
        10, "--users", "-c", help="Nombre d'utilisateurs à créer", min=1, max=1000
    ),
    min_vms: int = typer.Option(
        0, "--min-vms", help="Nombre minimum de VMs par utilisateur", min=0, max=10
    ),
    max_vms: int = typer.Option(
        3, "--max-vms", help="Nombre maximum de VMs par utilisateur", min=0, max=20
    ),
    admin_email: str = typer.Option(
        None, "--admin-email", "-a", help="Email de l'administrateur"
    ),
    admin_password: str = typer.Option(
        None, "--admin-password", "-p", help="Mot de passe de l'administrateur"
    ),
    export_file: str = typer.Option(
        "api_dataset.json", "--export", "-e", help="Fichier d'export du dataset"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    🌐 Créer un dataset directement via l'API avec des données Faker
    
    Crée des utilisateurs et des VMs directement via l'API externe avec des données réalistes.
    
    Exemples:
    
    \b
    python main.py api-generate --base-url "https://x8ki-letl-twmt.n7.xano.io/api:N1uLlTBt"
    python main.py api-generate -u "https://api.example.com" --users 25 --max-vms 5 --verbose
    """
    if min_vms > max_vms:
        typer.echo("❌ Le nombre minimum de VMs ne peut pas être supérieur au maximum")
        raise typer.Exit(1)
    
    typer.echo(f"🌐 Création d'un dataset via l'API {base_url}...")
    typer.echo(f"   • Utilisateurs: {user_count}")
    typer.echo(f"   • VMs par utilisateur: {min_vms}-{max_vms}")
    
    try:
        # Initialiser le service d'intégration
        service = APIIntegrationService(base_url, admin_email, admin_password)
        
        # Créer le dataset complet
        stats = service.create_full_dataset(user_count, (min_vms, max_vms))
        
        # Afficher les statistiques
        typer.echo(f"✅ Dataset créé avec succès via l'API !")
        typer.echo(f"📊 Statistiques:")
        typer.echo(f"   • Utilisateurs créés: {stats['users_created']}")
        typer.echo(f"   • VMs créées: {stats['vms_created']}")
        typer.echo(f"   • Total d'enregistrements: {stats['total_records']}")
        typer.echo(f"   • Utilisateurs avec VMs: {stats['users_with_vms']}")
        
        # Exporter le dataset si demandé
        try:
            export_data = service.export_dataset()
            output_path = Path(export_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data['dataset'], f, indent=4, ensure_asciique=False, default=str)
            
            typer.echo(f"📁 Dataset exporté vers: {output_path.absolute()}")
            
            if verbose:
                typer.echo(f"\n🔍 Aperçu des données créées:")
                for i, user in enumerate(export_data['dataset'][:3]):
                    typer.echo(f"   {i+1}. {user['name']} ({user['email']}) - {len(user['vms'])} VMs")
                if len(export_data['dataset']) > 3:
                    typer.echo(f"   ... et {len(export_data['dataset']) - 3} autres utilisateurs")
        except Exception as e:
            logger.warning("Impossible d'exporter le dataset", error=str(e))
            typer.echo(f"⚠️ Impossible d'exporter le dataset: {e}")
        
    except Exception as e:
        logger.error("Erreur lors de la création du dataset via l'API", error=str(e))
        typer.echo(f"❌ Erreur lors de la création du dataset via l'API: {e}")
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
