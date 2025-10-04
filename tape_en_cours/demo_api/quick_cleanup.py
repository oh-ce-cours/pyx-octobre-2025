#!/usr/bin/env python3
"""
Script de nettoyage simplifié pour les VMs et utilisateurs avec Typer et Rich
Utilise des fonctions modulaires pour une meilleure lisibilité
"""

import sys
import time
from typing import Optional, Tuple
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel

from utils.api import create_authenticated_client
from utils.logging_config import get_logger

# Configuration
app = typer.Typer(
    name="cleanup",
    help="🧹 Script de nettoyage pour les VMs et utilisateurs",
    rich_markup_mode="rich",
)
console = Console()
logger = get_logger(__name__)


# =============================================================================
# PARTIE REPRÉSENTATION / AFFICHAGE
# =============================================================================

def display_header(simulate: bool) -> None:
    """Affiche l'en-tête selon le mode"""
    if simulate:
        console.print(
            Panel.fit(
                "[bold blue]🧹 MODE SIMULATION[/bold blue]\n"
                "Aucune donnée ne sera supprimée",
                border_style="blue",
            )
        )
    else:
        console.print(
            Panel.fit(
                "[bold red]🗑️ MODE SUPPRESSION RÉELLE[/bold red]\n"
                "⚠️ TOUTES LES DONNÉES SERONT SUPPRIMÉES !",
                border_style="red",
            )
        )


def display_api_config(client) -> None:
    """Affiche la configuration de l'API"""
    config_table = Table(title="🔗 Configuration API")
    config_table.add_column("Paramètre", style="cyan")
    config_table.add_column("Valeur", style="magenta")

    config_table.add_row("Base URL", client.base_url)
    config_table.add_row(
        "Authentifié", "✅ Oui" if client.is_authenticated() else "❌ Non"
    )

    console.print(config_table)
    console.print()


def display_operation_config(delay: float, simulate: bool) -> None:
    """Affiche la configuration des opérations"""
    config_table = Table(title="🔧 Configuration")
    config_table.add_column("Paramètre", style="cyan")
    config_table.add_column("Valeur", style="magenta")
    config_table.add_row("Délai entre opérations", f"{delay}s")
    config_table.add_row("Mode", "Simulation" if simulate else "Suppression réelle")
    console.print(config_table)
    console.print()


def display_simulation_message() -> None:
    """Affiche le message de simulation"""
    console.print(
        Panel.fit(
            "[bold blue]📋 Mode simulation - aucune suppression réelle[/bold blue]\n"
            "Utilisez [bold]--real[/bold] pour effectuer les suppressions",
            border_style="blue",
        )
    )


# =============================================================================
# PARTIE MANIPULATION DES DONNÉES
# =============================================================================

def connect_to_api(
    base_url: Optional[str], email: Optional[str], password: Optional[str]
):
    """Se connecte à l'API et retourne le client"""
    with console.status("[bold green]Connexion à l'API..."):
        client = create_authenticated_client(base_url, email, password)
    return client


def fetch_data(client) -> Tuple[list, list]:
    """Récupère les données VMs et utilisateurs"""
    # Récupération VMs
    console.print("[bold cyan]📊 Données actuelles:[/bold cyan]")

    try:
        with console.status("[bold green]Récupérations des VMs..."):
            vms = client.vms.get()
        display_vms_table(vms)
        console.print()
    except Exception as e:
        console.print(f"[red]❌ Erreur VMs: {e}[/red]")
        vms = []

    # Récupération utilisateurs
    try:
        with console.status("[bold green]Récupération des utilisateurs..."):
            users = client.users.get()
        display_users_table(users)
        console.print()
    except Exception as e:
        console.print(f"[red]❌ Erreur Utilisateurs: {e}[/red]")
        users = []

    return vms, users


def display_vms_table(vms: list) -> None:
    """Affiche les VMs dans un tableau"""
    table = Table(title="💻 Machines virtuelles")
    table.add_column("ID", style="cyan")
    table.add_column("Nom", style="green")
    table.add_column("Utilisateur", style="yellow")
    table.add_column("Status", style="magenta")

    console.print(f"[green]✅ {len(vms)} VMs trouvées[/green]")

    for vm in vms:
        table.add_row(
            str(vm["id"]), vm["name"], str(vm["user_id"]), vm.get("status", "Inconnu")
        )

    console.print(table)


def display_users_table(users: list) -> None:
    """Affiche les utilisateurs dans un tableau"""
    table = Table(title="👥 Utilisateurs")
    table.add_column("ID", style="cyan")
    table.add_column("Nom", style="green")
    table.add_column("Email", style="yellow")

    console.print(f"[green]✅ {len(users)} utilisateurs trouvés[/green]")

    for user in users:
        table.add_row(str(user["id"]), user["name"], user["email"])

    console.print(table)


def display_deletion_progress(item_type: str, delay: float) -> None:
    """Affiche le panneau de suppression"""
    console.print(
        Panel.fit(
            f"[bold red]🗑️  Suppression des {item_type}s...[/bold red]\n"
            f"Délai: [bold]{delay}s[/bold]",
            border_style="red",
        )
    )


def display_deletion_result(item_type: str, deleted_count: int, total_count: int) -> None:
    """Affiche le résultat de suppression"""
    console.print(
        f"[bold cyan]📊 {item_type}s supprimés: [green]{deleted_count}/{total_count}[/green][/bold cyan]"
    )


def display_pause_message(delay: float, context: str = "") -> None:
    """Affiche un message de pause"""
    if context:
        console.print(f"[dim]⏱️  {context} ({delay}s)...[/dim]")
    else:
        console.print(f"[dim]⏱️  Pause de {delay}s...[/dim]")


def display_success_message(item_type: str, item_name: str) -> None:
    """Affiche un message de succès"""
    console.print(f"[green]✅ {item_type} supprimé: [bold]{item_name}[/bold][/green]")


def display_error_message(item_type: str, item_id: str, error: str) -> None:
    """Affiche un message d'erreur"""
    console.print(f"[red]❌ Erreur suppression {item_type} {item_id}: {error}[/red]")


def show_summary(vms: list, users: list, deleted_vms: int, deleted_users: int) -> None:
    """Affiche le résumé final"""
    total_deleted = deleted_vms + deleted_users

    summary_table = Table(title="🎯 Résumé du nettoyage")
    summary_table.add_column("Type", style="cyan")
    summary_table.add_column("Supprimé", style="green")
    summary_table.add_column("Total", style="yellow")

    summary_table.add_row("VMs", str(deleted_vms), str(len(vms)))
    summary_table.add_row("Utilisateurs", str(deleted_users), str(len(users)))
    summary_table.add_row(
        "**TOTAL**",
        f"[bold]{total_deleted}[/bold]",
        f"[bold]{len(vms) + len(users)}[/bold]",
    )

    console.print(summary_table)
    console.print(
        Panel.fit(
            "[bold green]✅ NETTOYAGE TERMINÉ AVEC SUCCÈS ![/bold green]",
            border_style="green",
        )
    )


# =============================================================================
# FONCTIONS PURES DE MANIPULATION DES DONNÉES
# =============================================================================

def delete_vm_data(client, vm: dict) -> bool:
    """Supprime une VM (logique pure sans affichage)"""
    try:
        client.vms.delete(vm["id"])
        return True
    except Exception:
        return False


def delete_user_data(client, user: dict) -> bool:
    """Supprime un utilisateur (logique pure sans affichage)"""
    try:
        client.users.delete_user(user["id"])
        return True
    except Exception:
        return False


def delete_items_batch(client, items: list, item_type: str, delay: float) -> int:
    """Supprime une liste d'éléments avec gestion des pauses
    
    Args:
        client: Client API
        items: Liste des éléments à supprimer
        item_type: Type d'élément ('vm' ou 'user')
        delay: Délai entre suppressions
        
    Returns:
        Nombre d'éléments supprimés
    """
    if not items:
        return 0

    deleted_count = 0
    
    for i, item in enumerate(items):
        # Suppression selon le type
        if item_type == "vm":
            success = delete_vm_data(client, item)
        else:  # user
            success = delete_user_data(client, item)
            
        if success:
            deleted_count += 1
            
        # Pause si pas le dernier élément
        if i < len(items) - 1:
            time.sleep(delay)
    
    # Pause supplémentaire avant prochaine section
    if deleted_count > 0 and item_type == "vm":
        time.sleep(delay + 1)
    
    return deleted_count


# =============================================================================
# FONCTIONS DE SUPPRESSION AVEC AFFICHAGE
# =============================================================================

def delete_items_with_progress(
    client, items: list, item_type: str, delay: float
) -> int:
    """Supprime des éléments avec barre de progression et affichage"""

    if not items:
        console.print(f"[yellow]⚠️  Aucun{item_type} à supprimer[/yellow]")
        return 0

    # Affichage du panneau de suppression
    display_deletion_progress(item_type, delay)

    deleted_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"Suppression de {len(items)} {item_type}s...", total=len(items)
        )

        for i, item in enumerate(items):
            # Suppression avec affichage
            if item_type == "vm":
                success = delete_single_vm_with_display(client, item)
            else:  # user
                success = delete_single_user_with_display(client, item)

            if success:
                deleted_count += 1

            progress.update(task, advance=1)

            # Pause si pas le dernier élément
            if i < len(items) - 1:
                display_pause_message(delay)

    # Affichage du résultat
    display_deletion_result(item_type, deleted_count, len(items))

    # Pause supplémentaire avant prochaine section
    if deleted_count > 0 and item_type == "vm":
        display_pause_message(delay + 1, "Pause avant les utilisateurs")

    return deleted_count


def delete_single_vm_with_display(client, vm: dict) -> bool:
    """Supprime une VM avec affichage"""
    try:
        with console.status(f"Suppression VM {vm['id']}: {vm['name']}..."):
            client.vms.delete(vm["id"])
        display_success_message("VM", vm['name'])
        return True
    except Exception as e:
        display_error_message("VM", vm['id'], str(e))
        return False


def delete_single_user_with_display(client, user: dict) -> bool:
    """Supprime un utilisateur avec affichage"""
    try:
        with console.status(f"Suppression utilisateur {user['id']}: {user['name']}..."):
            client.users.delete_user(user["id"])
        display_success_message("Utilisateur", user['name'])
        return True
    except Exception as e:
        display_error_message("User", user['id'], str(e))
        return False


# =============================================================================
# LOGIQUE MÉTIER PRINCIPALE
# =============================================================================

def cleanup_data(client, vms: list, users: list, delay: float) -> Tuple[int, int]:
    """Logique métier principale de nettoyage
    
    Args:
        client: Client API
        vms: Liste des VMs
        users: Liste des utilisateurs
        delay: Délai entre suppressions
        
    Returns:
        Tuple (deleted_vms, deleted_users)
    """
    # Suppression des VMs puis des utilisateurs
    deleted_vms = delete_items_with_progress(client, vms, "vm", delay)
    deleted_users = delete_items_with_progress(client, users, "user", delay)
    
    return deleted_vms, deleted_users


def show_summary(vms: list, users: list, deleted_vms: int, deleted_users: int) -> None:
    """Affiche le résumé final"""
    total_deleted = deleted_vms + deleted_users

    summary_table = Table(title="🎯 Résumé du nettoyage")
    summary_table.add_column("Type", style="cyan")
    summary_table.add_column("Supprimé", style="green")
    summary_table.add_column("Total", style="yellow")

    summary_table.add_row("VMs", str(deleted_vms), str(len(vms)))
    summary_table.add_row("Utilisateurs", str(deleted_users), str(len(users)))
    summary_table.add_row(
        "**TOTAL**",
        f"[bold]{total_deleted}[/bold]",
        f"[bold]{len(vms) + len(users)}[/bold]",
    )

    console.print(summary_table)
    console.print(
        Panel.fit(
            "[bold green]✅ NETTOYAGE TERMINÉ AVEC SUCCÈS ![/bold green]",
            border_style="green",
        )
    )


# =============================================================================
# FONCTION PRINCIPALE ORCHESTRANT TOUT
# =============================================================================

def quick_cleanup(
    base_url: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
    simulate: bool = True,
    delay: float = 2.5,
) -> None:
    """Fonction principale orchestrant le nettoyage"""
    try:
        # 1. AFFICHAGE - En-tête selon le mode
        display_header(simulate)

        # 2. DONNÉES - Connexion et récupération
        client = connect_to_api(base_url, email, password)
        display_api_config(client)
        vms, users = fetch_data(client)

        # 3. AFFICHAGE - Configuration des opérations
        display_operation_config(delay, simulate)

        # 4. LOGIQUE MÉTIER - Si simulation, arrêt ici
        if simulate:
            display_simulation_message()
            return

        # 5. LOGIQUE MÉTIER - Suppressions réelles
        deleted_vms, deleted_users = cleanup_data(client, vms, users, delay)

        # 6. AFFICHAGE - Résumé final
        show_summary(vms, users, deleted_vms, deleted_users)

    except Exception as e:
        console.print(f"[bold red]❌ Erreur critique: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def cleanup(
    base_url: Optional[str] = typer.Option(
        None, "--base-url", "-u", help="URL de base de l'API"
    ),
    email: Optional[str] = typer.Option(
        None, "--email", "-e", help="Email pour l'authentification"
    ),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", help="Mot de passe pour l'authentification"
    ),
    real: bool = typer.Option(
        False, "--real", "-r", help="Effectue la suppression réelle"
    ),
    delay: float = typer.Option(
        2.5, "--delay", "-d", help="Délai en secondes entre les opérations"
    ),
) -> None:
    """
    Script de nettoyage pour les VMs et utilisateurs

    💡 Exemples d'usage:

    • Mode simulation (par défaut):
       python quick_cleanup_simplified.py

    • Suppression réelle:
       python quick_cleanup_simplified.py --real

    • Avec délai personnalisé:
       python quick_cleanup_simplified.py --real --delay 3
    """
    simulate = not real
    quick_cleanup(base_url, email, password, simulate, delay)


def main():
    """Point d'entrée principal"""
    app()


if __name__ == "__main__":
    main()
