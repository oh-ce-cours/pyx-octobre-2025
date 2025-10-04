#!/usr/bin/env python3
"""
Script pour créer des données via l'API en utilisant le générateur Faker.

Ce script utilise l'API unifiée pour créer des utilisateurs et des VMs
avec des données générées par Faker, permettant de peupler la base de données
avec des données réalistes.
"""

import typer
import time
import sys
from typing import Optional, List, Dict, Any
from pathlib import Path
import json
from datetime import datetime
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.panel import Panel

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.api import ApiClient
from utils.data_generator import UserDataGenerator, VMDataGenerator
from utils.logging_config import get_logger

logger = get_logger(__name__)
console = Console()

app = typer.Typer(
    name="create-data-via-api",
    help="🚀 Créateur de données via API avec Faker",
    rich_markup_mode="rich",
    add_completion=False,
    no_args_is_help=True,
)


# =============================================================================
# PARTIE REPRÉSENTATION / AFFICHAGE
# =============================================================================


def display_header(title: str, subtitle: str = "") -> None:
    """Affiche l'en-tête principal"""
    header_text = f"[bold blue]{title}[/bold blue]"
    if subtitle:
        header_text += f"\n[dim]{subtitle}[/dim]"

    console.print(
        Panel.fit(
            header_text,
            border_style="blue",
        )
    )


def display_api_config(client: ApiClient) -> None:
    """Affiche la configuration de l'API"""
    config_table = Table(title="🔗 Configuration API")
    config_table.add_column("Paramètre", style="cyan")
    config_table.add_column("Valeur", style="magenta")

    config_table.add_row("Base URL", client.base_url)
    config_table.add_row("Mode", "Client simple")

    console.print(config_table)
    console.print()


def display_operation_config(
    operation: str, count: int, batch_size: int, delay: float
) -> None:
    """Affiche la configuration des opérations"""
    config_table = Table(title=f"🔧 Configuration - {operation}")
    config_table.add_column("Paramètre", style="cyan")
    config_table.add_column("Valeur", style="magenta")

    config_table.add_row("Nombre total", str(count))
    config_table.add_row("Taille des lots", str(batch_size))
    config_table.add_row("Délai entre lots", f"{delay}s")

    console.print(config_table)
    console.print()


def display_batch_progress(batch_num: int, start: int, end: int, total: int) -> None:
    """Affiche le progrès d'un lot"""
    console.print(
        f"[bold cyan]📝 Lot {batch_num}:[/bold cyan] éléments {start + 1}-{end} sur {total}"
    )


def display_success_message(
    item_type: str, item_name: str, item_details: str = ""
) -> None:
    """Affiche un message de succès"""
    message = f"[green]✅ {item_type} créé:[/green] [bold]{item_name}[/bold]"
    if item_details:
        message += f" [dim]({item_details})[/dim]"
    console.print(message)


def display_error_message(item_type: str, item_index: int, error: str) -> None:
    """Affiche un message d'erreur"""
    console.print(f"[red]❌ Erreur {item_type} {item_index + 1}:[/red] {error}")


def display_statistics(title: str, stats: Dict[str, Any]) -> None:
    """Affiche les statistiques dans un tableau"""
    stats_table = Table(title=f"📊 {title}")
    stats_table.add_column("Métrique", style="cyan")
    stats_table.add_column("Valeur", style="green")

    for key, value in stats.items():
        stats_table.add_row(key, str(value))

    console.print(stats_table)
    console.print()


def display_preview(
    title: str, items: List[Dict[str, Any]], max_items: int = 5
) -> None:
    """Affiche un aperçu des éléments créés"""
    if not items:
        return

    console.print(f"[bold cyan]🔍 {title}:[/bold cyan]")

    for i, item in enumerate(items[:max_items]):
        if "name" in item and "email" in item:
            # Utilisateur
            console.print(f"   {i + 1}. [bold]{item['name']}[/bold] ({item['email']})")
        elif "name" in item and "operating_system" in item:
            # VM
            console.print(
                f"   {i + 1}. [bold]{item['name']}[/bold] ({item['operating_system']})"
            )
        else:
            console.print(f"   {i + 1}. {item}")

    if len(items) > max_items:
        console.print(f"   ... et {len(items) - max_items} autres éléments")

    console.print()


def display_dataset_saved(file_path: Path) -> None:
    """Affiche le message de sauvegarde du dataset"""
    console.print(
        Panel.fit(
            f"[bold green]💾 Dataset sauvegardé:[/bold green]\n{file_path.absolute()}",
            border_style="green",
        )
    )


def display_api_status(all_data: Dict[str, Any], api_url: str) -> None:
    """Affiche le statut de l'API"""
    status_table = Table(title="📊 Statut de l'API")
    status_table.add_column("Métrique", style="cyan")
    status_table.add_column("Valeur", style="green")

    status_table.add_row("URL de l'API", api_url)
    status_table.add_row("Utilisateurs total", str(all_data["total_users"]))
    status_table.add_row("VMs totales", str(all_data["total_vms"]))
    status_table.add_row("Utilisateurs avec VMs", str(all_data["users_with_vms"]))

    if all_data["total_users"] > 0:
        avg_vms = all_data["total_vms"] / all_data["total_users"]
        status_table.add_row("Moyenne VMs/utilisateur", f"{avg_vms:.1f}")

    console.print(status_table)
    console.print()


# =============================================================================
# PARTIE LOGIQUE MÉTIER / DONNÉES
# =============================================================================


def create_users_via_api(
    api_client: ApiClient,
    user_count: int,
    batch_size: int = 10,
    delay_between_batches: float = 0.5,
) -> List[Dict[str, Any]]:
    """
    Crée des utilisateurs via l'API en utilisant le générateur Faker.

    Args:
        api_client: Client API authentifié
        user_count: Nombre d'utilisateurs à créer
        batch_size: Nombre d'utilisateurs à créer par lot
        delay_between_batches: Délai entre les lots (en secondes)

    Returns:
        Liste des utilisateurs créés
    """
    logger.info(
        "Création d'utilisateurs via API", count=user_count, batch_size=batch_size
    )

    created_users = []
    created_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"Création de {user_count} utilisateurs...", total=user_count
        )

        for batch_start in range(0, user_count, batch_size):
            batch_end = min(batch_start + batch_size, user_count)
            batch_size_actual = batch_end - batch_start

            display_batch_progress(
                batch_start // batch_size + 1, batch_start, batch_end, user_count
            )

            for i in range(batch_size_actual):
                try:
                    # Générer les données utilisateur avec Faker
                    user_data = UserDataGenerator.generate_user(created_count + 1)

                    # Créer l'utilisateur via l'API (retry automatique via décorateur)
                    created_user = api_client.users.create_user(
                        name=user_data["name"],
                        email=user_data["email"],
                        password="password123",  # Mot de passe par défaut
                    )
                    
                    # Vérifier que l'utilisateur a été créé avec succès
                    if created_user and isinstance(created_user, dict) and "id" in created_user:
                        created_users.append(created_user)
                        created_count += 1
                        display_success_message(
                            "Utilisateur", user_data["name"], user_data["email"]
                        )
                    else:
                        logger.error(
                            "Échec de création d'utilisateur - données invalides",
                            user_data=user_data,
                            created_user=created_user
                        )
                        display_error_message("utilisateur", i, "Données utilisateur invalides")

                except (ValueError, KeyError, ConnectionError) as e:
                    logger.error(
                        "Erreur lors de la création d'un utilisateur", error=str(e)
                    )
                    display_error_message("utilisateur", i, str(e))

                progress.update(task, advance=1)

                # Délai entre chaque création d'utilisateur
                if i < batch_size_actual - 1 or batch_end < user_count:
                    time.sleep(delay_between_batches / 2)

            # Délai entre les lots pour éviter de surcharger l'API
            if batch_end < user_count:
                time.sleep(delay_between_batches)

    logger.info("Utilisateurs créés avec succès", count=len(created_users))
    return created_users


def create_vms_via_api(
    api_client: ApiClient,
    vm_count: int,
    user_ids: List[int],
    batch_size: int = 10,
    delay_between_batches: float = 0.5,
) -> List[Dict[str, Any]]:
    """
    Crée des VMs via l'API en utilisant le générateur Faker.

    Args:
        api_client: Client API authentifié
        vm_count: Nombre de VMs à créer
        user_ids: Liste des IDs d'utilisateurs disponibles
        batch_size: Nombre de VMs à créer par lot
        delay_between_batches: Délai entre les lots (en secondes)

    Returns:
        Liste des VMs créées
    """
    logger.info(
        "Création de VMs via API", count=vm_count, available_users=len(user_ids)
    )

    created_vms = []
    created_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(f"Création de {vm_count} VMs...", total=vm_count)

        for batch_start in range(0, vm_count, batch_size):
            batch_end = min(batch_start + batch_size, vm_count)
            batch_size_actual = batch_end - batch_start

            display_batch_progress(
                batch_start // batch_size + 1, batch_start, batch_end, vm_count
            )

            for i in range(batch_size_actual):
                try:
                    # Générer les données VM avec Faker
                    vm_data = VMDataGenerator.generate_vm(
                        user_id=user_ids[created_count % len(user_ids)],
                        vm_id=created_count + 1,
                    )

                    # Créer la VM via l'API (retry automatique via décorateur)
                    created_vm = api_client.vms.create(
                        user_id=vm_data["user_id"],
                        name=vm_data["name"],
                        operating_system=vm_data["operating_system"],
                        cpu_cores=vm_data["cpu_cores"],
                        ram_gb=vm_data["ram_gb"],
                        disk_gb=vm_data["disk_gb"],
                        status=vm_data["status"],
                    )
                    created_vms.append(created_vm)
                    created_count += 1

                    vm_details = f"{vm_data['operating_system']} - {vm_data['cpu_cores']}c/{vm_data['ram_gb']}GB"
                    display_success_message("VM", vm_data["name"], vm_details)

                except (ValueError, KeyError, ConnectionError) as e:
                    logger.error("Erreur lors de la création d'une VM", error=str(e))
                    display_error_message("VM", i, str(e))

                progress.update(task, advance=1)

                # Délai entre chaque création de VM
                if i < batch_size_actual - 1 or batch_end < vm_count:
                    time.sleep(delay_between_batches / 2)

            # Délai entre les lots pour éviter de surcharger l'API
            if batch_end < vm_count:
                time.sleep(delay_between_batches)

    logger.info("VMs créées avec succès", count=len(created_vms))
    return created_vms


# =============================================================================
# COMMANDES TYPER AVEC AFFICHAGE RICH
# =============================================================================


@app.command()
def users(
    count: int = typer.Option(
        10, "--count", "-c", help="Nombre d'utilisateurs à créer", min=1, max=100
    ),
    batch_size: int = typer.Option(
        5, "--batch-size", "-b", help="Taille des lots", min=1, max=20
    ),
    delay: float = typer.Option(
        2.0, "--delay", "-d", help="Délai entre les lots (secondes)", min=0.5, max=10.0
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    👥 Créer des utilisateurs via l'API avec des données Faker

    Génère des utilisateurs réalistes avec Faker et les crée via l'API.

    Exemples:

    \b
    python create_data_via_api.py users --count 20
    python create_data_via_api.py users -c 50 --batch-size 10 --delay 3.0 --max-retries 7
    python create_data_via_api.py users --verbose
    """
    display_header(
        "👥 Création d'utilisateurs via l'API",
        f"Génération de {count} utilisateurs avec Faker",
    )

    try:
        # Créer le client API simple
        api_client = ApiClient()

        console.print(
            f"[bold green]🔗 Connexion à l'API sur {api_client.base_url}[/bold green]"
        )
        console.print()

        # Afficher la configuration
        display_api_config(api_client)
        display_operation_config("Utilisateurs", count, batch_size, delay)

        # Créer les utilisateurs
        created_users = create_users_via_api(
            api_client=api_client,
            user_count=count,
            batch_size=batch_size,
            delay_between_batches=delay,
        )

        # Statistiques
        stats = {
            "Utilisateurs créés": len(created_users),
            "Taux de succès": f"{len(created_users) / count * 100:.1f}%",
        }
        display_statistics("Résultat de la création", stats)

        if verbose and created_users:
            display_preview("Aperçu des utilisateurs créés", created_users)

        console.print(
            Panel.fit(
                "[bold green]✅ CRÉATION TERMINÉE AVEC SUCCÈS ![/bold green]",
                border_style="green",
            )
        )

    except Exception as e:
        logger.error("Erreur lors de la création des utilisateurs", error=str(e))
        console.print(
            Panel.fit(
                f"[bold red]❌ Erreur lors de la création:[/bold red]\n{e}",
                border_style="red",
            )
        )
        raise typer.Exit(1)


@app.command()
def vms(
    count: int = typer.Option(
        20, "--count", "-c", help="Nombre de VMs à créer", min=1, max=200
    ),
    batch_size: int = typer.Option(
        5, "--batch-size", "-b", help="Taille des lots", min=1, max=20
    ),
    delay: float = typer.Option(
        2.0, "--delay", "-d", help="Délai entre les lots (secondes)", min=0.5, max=10.0
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    🖥️ Créer des VMs via l'API avec des données Faker

    Génère des VMs réalistes avec Faker et les crée via l'API.
    Les VMs sont associées à des utilisateurs existants.

    Exemples:

    \b
    python create_data_via_api.py vms --count 50
    python create_data_via_api.py vms -c 100 --batch-size 10 --delay 3.0
    python create_data_via_api.py vms --verbose
    """
    display_header(
        "🖥️ Création de VMs via l'API", f"Génération de {count} VMs avec Faker"
    )

    try:
        # Créer le client API simple
        api_client = ApiClient()

        console.print(
            f"[bold green]🔗 Connexion à l'API sur {api_client.base_url}[/bold green]"
        )
        console.print()

        # Afficher la configuration
        display_api_config(api_client)

        # Récupérer les utilisateurs existants
        with console.status("[bold green]Récupération des utilisateurs existants..."):
            existing_users = api_client.users.get()

        if not existing_users:
            console.print(
                Panel.fit(
                    "[bold red]❌ Aucun utilisateur trouvé dans l'API[/bold red]\n"
                    "[dim]💡 Créez d'abord des utilisateurs avec la commande 'users'[/dim]",
                    border_style="red",
                )
            )
            raise typer.Exit(1)

        user_ids = [user["id"] for user in existing_users]
        console.print(
            f"[bold cyan]👥 {len(user_ids)} utilisateurs disponibles pour l'association des VMs[/bold cyan]"
        )
        console.print()

        display_operation_config("VMs", count, batch_size, delay)

        # Créer les VMs
        created_vms = create_vms_via_api(
            api_client=api_client,
            vm_count=count,
            user_ids=user_ids,
            batch_size=batch_size,
            delay_between_batches=delay,
        )

        # Statistiques
        stats = {
            "VMs créées": len(created_vms),
            "Taux de succès": f"{len(created_vms) / count * 100:.1f}%",
            "Utilisateurs concernés": len(user_ids),
        }
        display_statistics("Résultat de la création", stats)

        if verbose and created_vms:
            display_preview("Aperçu des VMs créées", created_vms)

        console.print(
            Panel.fit(
                "[bold green]✅ CRÉATION TERMINÉE AVEC SUCCÈS ![/bold green]",
                border_style="green",
            )
        )

    except Exception as e:
        logger.error("Erreur lors de la création des VMs", error=str(e))
        console.print(
            Panel.fit(
                f"[bold red]❌ Erreur lors de la création:[/bold red]\n{e}",
                border_style="red",
            )
        )
        raise typer.Exit(1)


@app.command()
def full_dataset(
    user_count: int = typer.Option(
        20, "--users", "-u", help="Nombre d'utilisateurs à créer", min=1, max=100
    ),
    vm_count: int = typer.Option(
        50, "--vms", "-v", help="Nombre de VMs à créer", min=1, max=200
    ),
    batch_size: int = typer.Option(
        5, "--batch-size", "-b", help="Taille des lots", min=1, max=20
    ),
    delay: float = typer.Option(
        2.0, "--delay", "-d", help="Délai entre les lots (secondes)", min=0.5, max=10.0
    ),
    output_file: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Fichier de sortie pour sauvegarder les données créées",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    🎯 Créer un dataset complet via l'API avec des données Faker

    Crée des utilisateurs et des VMs réalistes avec Faker via l'API.
    Optionnellement sauvegarde les données créées dans un fichier JSON.

    Exemples:

    \b
    python create_data_via_api.py full-dataset --users 20 --vms 50
    python create_data_via_api.py full-dataset -u 30 -v 100 --delay 3.0 --output dataset.json
    python create_data_via_api.py full-dataset --verbose
    """
    display_header(
        "🎯 Création d'un dataset complet",
        f"{user_count} utilisateurs + {vm_count} VMs avec Faker",
    )

    try:
        # Créer le client API simple
        api_client = ApiClient()

        console.print(
            f"[bold green]🔗 Connexion à l'API sur {api_client.base_url}[/bold green]"
        )
        console.print()

        # Afficher la configuration
        display_api_config(api_client)
        display_operation_config(
            "Dataset complet", user_count + vm_count, batch_size, delay
        )

        # Étape 1: Créer les utilisateurs
        console.print(
            Panel.fit(
                f"[bold blue]👥 Étape 1/2: Création de {user_count} utilisateurs[/bold blue]",
                border_style="blue",
            )
        )
        created_users = create_users_via_api(
            api_client=api_client,
            user_count=user_count,
            batch_size=batch_size,
            delay_between_batches=delay,
        )

        # Étape 2: Créer les VMs
        console.print(
            Panel.fit(
                f"[bold blue]🖥️ Étape 2/2: Création de {vm_count} VMs[/bold blue]",
                border_style="blue",
            )
        )
        user_ids = [user["id"] for user in created_users]
        created_vms = create_vms_via_api(
            api_client=api_client,
            vm_count=vm_count,
            user_ids=user_ids,
            batch_size=batch_size,
            delay_between_batches=delay,
        )

        # Statistiques finales
        stats = {
            "Utilisateurs créés": len(created_users),
            "VMs créées": len(created_vms),
            "Taux de succès utilisateurs": f"{len(created_users) / user_count * 100:.1f}%",
            "Taux de succès VMs": f"{len(created_vms) / vm_count * 100:.1f}%",
        }
        display_statistics("Statistiques finales", stats)

        # Sauvegarder les données si demandé
        if output_file:
            dataset = {
                "created_at": datetime.now().isoformat(),
                "users": created_users,
                "vms": created_vms,
                "statistics": {
                    "total_users": len(created_users),
                    "total_vms": len(created_vms),
                    "user_success_rate": len(created_users) / user_count * 100,
                    "vm_success_rate": len(created_vms) / vm_count * 100,
                },
            }

            output_path = Path(output_file)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(dataset, f, indent=4, ensure_ascii=False, default=str)

            display_dataset_saved(output_path)

        if verbose:
            display_preview("Aperçu des utilisateurs créés", created_users, 3)
            display_preview("Aperçu des VMs créées", created_vms, 3)

        console.print(
            Panel.fit(
                "[bold green]✅ DATASET CRÉÉ AVEC SUCCÈS ![/bold green]",
                border_style="green",
            )
        )

    except Exception as e:
        logger.error("Erreur lors de la création du dataset", error=str(e))
        console.print(
            Panel.fit(
                f"[bold red]❌ Erreur lors de la création:[/bold red]\n{e}",
                border_style="red",
            )
        )
        raise typer.Exit(1)


@app.command()
def status() -> None:
    """
    📊 Afficher le statut actuel de l'API

    Récupère et affiche les statistiques actuelles des utilisateurs et VMs.

    Exemples:

    \b
    python create_data_via_api.py status
    """
    display_header("📊 Statut de l'API", "Récupération des statistiques actuelles")

    try:
        # Créer le client API simple
        api_client = ApiClient()

        console.print(
            f"[bold green]🔗 Connexion à l'API sur {api_client.base_url}[/bold green]"
        )
        console.print()

        # Afficher la configuration
        display_api_config(api_client)

        # Récupérer toutes les données
        with console.status("[bold green]Récupération des données..."):
            all_data = api_client.get_all_data()

        # Afficher les statistiques
        display_api_status(all_data, api_client.base_url)

        console.print(
            Panel.fit(
                "[bold green]✅ STATUT RÉCUPÉRÉ AVEC SUCCÈS ![/bold green]",
                border_style="green",
            )
        )

    except Exception as e:
        logger.error("Erreur lors de la récupération du statut", error=str(e))
        console.print(
            Panel.fit(
                f"[bold red]❌ Erreur lors de la récupération:[/bold red]\n{e}",
                border_style="red",
            )
        )
        raise typer.Exit(1)


@app.command()
def version() -> None:
    """📋 Afficher la version du créateur de données"""
    console.print(
        Panel.fit(
            "[bold blue]create-data-via-api v1.0.0[/bold blue]\n"
            "[dim]Powered by Faker 🎲 + API unifiée 🚀[/dim]",
            border_style="blue",
        )
    )


def main():
    """Point d'entrée principal"""

    # Gérer -h comme alias pour --help
    if "-h" in sys.argv and "--help" not in sys.argv:
        sys.argv[sys.argv.index("-h")] = "--help"

    try:
        app()
    except KeyboardInterrupt:
        console.print(
            Panel.fit(
                "[bold yellow]⚠️ Création interrompue[/bold yellow]",
                border_style="yellow",
            )
        )
    except Exception as e:
        console.print(
            Panel.fit(
                f"[bold red]❌ Erreur:[/bold red]\n{e}",
                border_style="red",
            )
        )
        raise typer.Exit(1)


if __name__ == "__main__":
    main()
