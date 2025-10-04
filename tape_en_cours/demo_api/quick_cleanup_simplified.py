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
    rich_markup_mode="rich"
)
console = Console()
logger = get_logger(__name__)


def display_header(simulate: bool) -> None:
    """Affiche l'en-tête selon le mode"""
    if simulate:
        console.print(Panel.fit(
            "[bold blue]🧹 MODE SIMULATION[/bold blue]\n"
            "Aucune donnée ne sera supprimée",
            border_style="blue"
        ))
    else:
        console.print(Panel.fit(
            "[bold red]🗑️ MODE SUPPRESSION RÉELLE[/bold red]\n"
            "⚠️ TOUTES LES DONNÉES SERONT SUPPRIMÉES !",
            border_style="red"
        ))


def connect_to_api(base_url: Optional[str], email: Optional[str], password: Optional[str]):
    """Se connecte à l'API et retourne le client"""
    with console.status("[bold green]Connexion à l'API..."):
        client = create_authenticated_client(base_url, email, password)
    
    # Affichage configuration API
    config_table = Table(title="🔗 Configuration API")
    config_table.add_column("Paramètre", style="cyan")
    config_table.add_column("Valeur", style="magenta")
    
    config_table.add_row("Base URL", client.base_url)
    config_table.add_row("Authentifié", "✅ Oui" if client.is_authenticated() else "❌ Non")
    
    console.print(config_table)
    console.print()
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
            str(vm['id']), 
            vm['name'], 
            str(vm['user_id']), 
            vm.get('status', 'Inconnu')
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
        table.add_row(str(user['id']), user['name'], user['email'])
    
    console.print(table)


def delete_items_with_progress(client, items: list, item_type: str, delay: float) -> int:
    """Supprime des éléments avec barre de progression
    
    Args:
        client: Client API
        items: Liste des éléments à supprimer
        item_type: Type d'élément ('vm' ou 'user')
        delay: Délai entre suppressions
        
    Returns:
        Nombre d'éléments supprimés
    """
    if not items:
        console.print(f"[yellow]⚠️  Aucun{item_type} à supprimer[/yellow]")
        return 0

    deleted_count = 0
    
    console.print(Panel.fit(
        f"[bold red]🗑️  Suppression des {item_type}s...[/bold red]\n"
        f"Délai: [bold]{delay}s[/bold]",
        border_style="red"
    ))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Suppression de {len(items)} {item_type}s...", total=len(items))
        
        for i, item in enumerate(items):
            if item_type == "vm":
                success = delete_single_vm(client, item)
            else:  # user
                success = delete_single_user(client, item)
                
            if success:
                deleted_count += 1
                
            progress.update(task, advance=1)
            
            # Pause si pas le dernier élément
            if i < len(items) - 1:
                console.print(f"[dim]⏱️  Pause de {delay}s...[/dim]")
                time.sleep(delay)

    console.print(f"[bold cyan]📊 {item_type}s supprimés: [green]{deleted_count}/{len(items)}[/green][/bold cyan]")
    
    # Pause supplémentaire avant prochaine section
    if deleted_count > 0 and item_type == "vm":
        console.print(f"[dim]⏱️  Pause de {delay + 1}s avant les utilisateurs...[/dim]")
        time.sleep(delay + 1)
    
    return deleted_count


def delete_single_vm(client, vm: dict) -> bool:
    """Supprime une VM individuelle"""
    try:
        with console.status(f"Suppression VM {vm['id']}: {vm['name']}..."):
            client.vms.delete(vm["id"])
        console.print(f"[green]✅ VM supprimée: [bold]{vm['name']}[/bold][/green]")
        return True
    except Exception as e:
        console.print(f"[red]❌ Erreur suppression VM {vm['id']}: {e}[/red]")
        return False


def delete_single_user(client, user: dict) -> bool:
    """Supprime un utilisateur individuel"""
    try:
        with console.status(f"Suppression utilisateur {user['id']}: {user['name']}..."):
            client.users.delete_user(user["id"])
        console.print(f"[green]✅ Utilisateur supprimé: [bold]{user['name']}[/bold][/green]")
        return True
    except Exception as e:
        console.print(f"[red]❌ Erreur suppression User {user['id']}: {e}[/red]")
        return False


def show_summary(vms: list, users: list, deleted_vms: int, deleted_users: int) -> None:
    """Affiche le résumé final"""
    total_deleted = deleted_vms + deleted_users
    
    summary_table = Table(title="🎯 Résumé du nettoyage")
    summary_table.add_column("Type", style="cyan")
    summary_table.add_column("Supprimé", style="green")
    summary_table.add_column("Total", style="yellow")
    
    summary_table.add_row("VMs", str(deleted_vms), str(len(vms)))
    summary_table.add_row("Utilisateurs", str(deleted_users), str(len(users)))
    summary_table.add_row("**TOTAL**", f"[bold]{total_deleted}[/bold]", 
                         f"[bold]{len(vms) + len(users)}[/bold]")
    
    console.print(summary_table)
    console.print(Panel.fit(
        "[bold green]✅ NETTOYAGE TERMINÉ AVEC SUCCÈS ![/bold green]",
        border_style="green"
    ))


def quick_cleanup(
    base_url: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
    simulate: bool = True,
    delay: float = 2.5,
) -> None:
    """Fonction principale de nettoyage"""
    try:
        # Affichage de l'en-tête
        display_header(simulate)
        
        # Connexion et récupération des données
        client = connect_to_api(base_url, email, password)
        vms, users = fetch_data(client)
        
        # Configuration table
        config_table = Table(title="🔧 Configuration")
        config_table.add_column("Paramètre", style="cyan")
        config_table.add_column("Valeur", style="magenta")
        config_table.add_row("Délai entre opérations", f"{delay}s")
        config_table.add_row("Mode", "Simulation" if simulate else "Suppression réelle")
        console.print(config_table)
        console.print()
        
        # Si simulation, arrêt ici
        if simulate:
            console.print(Panel.fit(
                "[bold blue]📋 Mode simulation - aucune suppression réelle[/bold blue]\n"
                "Utilisez [bold]--real[/bold] pour effectuer les suppressions",
                border_style="blue"
            ))
            return
        
        # Suppressions réelles
        deleted_vms = delete_items_with_progress(client, vms, "vm", delay)
        deleted_users = delete_items_with_progress(client, users, "user", delay)
        
        # Résumé final
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
    )
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
