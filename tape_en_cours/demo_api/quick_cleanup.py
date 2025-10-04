#!/usr/bin/env python3
"""
Script de nettoyage rapide et simple pour les VMs et utilisateurs
"""

import time
from typing import Optional
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel

from utils.api import create_authenticated_client
from utils.logging_config import get_logger

# Configuration Rich et Typer
app = typer.Typer(
    name="cleanup",
    help="🧹 Script de nettoyage pour les VMs et utilisateurs",
    rich_markup_mode="rich",
)
console = Console()

logger = get_logger(__name__)


def quick_cleanup(
    base_url: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
    simulate: bool = True,
    delay: float = 2.5,
) -> None:
    """
    Nettoie rapidement toutes les données avec respect des limites de taux

    Args:
        base_url: URL de base de l'API (optionnel)
        email: Email pour l'authentification (optionnel)
        password: Mot de passe pour l'authentification (optionnel)
        simulate: Si True, mode simulation (aucune suppression réelle)
        delay: Délai en secondes entre les suppressions pour éviter les 429
    """

    # Affichage du mode avec Rich
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
                "[bold red]🗑️  MODE SUPPRESSION RÉELLE[/bold red]\n"
                "⚠️  TOUTES LES DONNÉES SERONT SUPPRIMÉES !",
                border_style="red",
            )
        )

    try:
        # Connexion à l'API avec spinner
        with console.status("[bold green]Connexion à l'API...") as status:
            client = create_authenticated_client(base_url, email, password)
            status.update("[bold green]Connexion établie !")

        # Affichage des infos de connexion
        table = Table(title="🔗 Configuration API")
        table.add_column("Paramètre", style="cyan")
        table.add_column("Valeur", style="magenta")

        table.add_row("Base URL", client.base_url)
        table.add_row(
            "Authentifié", "✅ Oui" if client.is_authenticated() else "❌ Non"
        )
        table.add_row("Délai entre opérations", f"{delay}s")
        table.add_row("Mode", "Simulation" if simulate else "Suppression réelle")

        console.print(table)
        console.print()

        # Récupérer les données actuelles avec Rich
        console.print("[bold cyan]📊 Données actuelles:[/bold cyan]")

        # Tableau des VMs
        vms_table = Table(title="💻 Machines virtuelles")
        vms_table.add_column("ID", style="cyan")
        vms_table.add_column("Nom", style="green")
        vms_table.add_column("Utilisateur", style="yellow")
        vms_table.add_column("Status", style="magenta")

        try:
            with console.status("[bold green]Récupérations des VMs...") as status:
                vms = client.vms.get()

            console.print(f"[green]✅ {len(vms)} VMs trouvées[/green]")

            for vm in vms:
                vms_table.add_row(
                    str(vm["id"]),
                    vm["name"],
                    str(vm["user_id"]),
                    vm.get("status", "Inconnu"),
                )

        except Exception as e:
            console.print(f"[red]❌ Erreur VMs: {e}[/red]")
            vms = []

        console.print(vms_table)
        console.print()

        # Tableau des utilisateurs
        users_table = Table(title="👥 Utilisateurs")
        users_table.add_column("ID", style="cyan")
        users_table.add_column("Nom", style="green")
        users_table.add_column("Email", style="yellow")

        try:
            with console.status(
                "[bold green]Récupération des utilisateurs..."
            ) as status:
                users = client.users.get()

            console.print(f"[green]✅ {len(users)} utilisateurs trouvés[/green]")

            for user in users:
                users_table.add_row(str(user["id"]), user["name"], user["email"])

        except Exception as e:
            console.print(f"[red]❌ Erreur Utilisateurs: {e}[/red]")
            users = []

        console.print(users_table)
        console.print()

        if simulate:
            console.print(
                Panel.fit(
                    "[bold blue]📋 Mode simulation - aucune suppression réelle[/bold blue]\n"
                    "Utilisez [bold]--real[/bold] pour effectuer les suppressions",
                    border_style="blue",
                )
            )
            return

        # Suppression réelle avec progress bar
        console.print(
            Panel.fit(
                f"[bold red]🗑️  SUPPRESSION RÉELLE EN cours...[/bold red]\n"
                f"Délai entre opérations: [bold]{delay}s[/bold]",
                border_style="red",
            )
        )

        # Supprimer les VMs d'abord
        try:
            with console.status(
                "[bold green]Récupération des VMs pour suppression..."
            ) as status:
                vms = client.vms.get()

            if not vms:
                console.print("[yellow]⚠️  Aucune VM à supprimer[/yellow]")
                deleted_vms = 0
            else:
                deleted_vms = 0

                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console,
                ) as progress:
                    task = progress.add_task(
                        f"Suppression de {len(vms)} VMs...", total=len(vms)
                    )

                    for i, vm in enumerate(vms):
                        try:
                            with console.status(
                                f"Suppression VM {vm['id']}: {vm['name']}..."
                            ) as delete_status:
                                client.vms.delete(vm["id"])

                            console.print(
                                f"[green]✅ VM supprimée ({i + 1}/{len(vms)}): [bold]{vm['name']}[/bold][/green]"
                            )
                            deleted_vms += 1
                            progress.update(task, advance=1)

                            # Pause entre les suppressions
                            if i < len(vms) - 1:
                                console.print(f"[dim]⏱️  Pause de {delay}s...[/dim]")
                                time.sleep(delay)

                        except Exception as e:
                            console.print(
                                f"[red]❌ Erreur suppression VM {vm['id']}: {e}[/red]"
                            )
                            progress.update(task, advance=1)

                            # Pause même en cas d'erreur
                            if i < len(vms) - 1:
                                console.print(
                                    f"[dim]⏱️  Pause après erreur ({delay}s)...[/dim]"
                                )
                                time.sleep(delay)

            console.print(
                f"[bold cyan]📊 Résultat VMs: [green]{deleted_vms}/{len(vms)} supprimées[/green][/bold cyan]"
            )

            # Pause avant utilisateurs
            if deleted_vms > 0:
                console.print(
                    f"[dim]⏱️  Pause de {delay + 1}s avant les utilisateurs...[/dim]"
                )
                time.sleep(delay + 1)

        except Exception as e:
            console.print(f"[red]❌ Erreur lors de la récupération des VMs: {e}[/red]")

        # Supprimer les utilisateurs ensuite
        try:
            with console.status("[bold green]Récupération des utilisateurs pour suppression...") as status:
                users = client.users.get()
            
            if not users:
                console.print("[yellow]⚠️  Aucun utilisateur à supprimer[/yellow]")
                deleted_users = 0
            else:
                deleted_users = 0
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task(f"Suppression de {len(users)} utilisateurs...", total=len(users))
                    
                    for i, user in enumerate(users):
                        try:
                            with console.status(f"Suppression utilisateur {user['id']}: {user['name']}...") as delete_status:
                                client.users.delete_user(user["id"])
                                
                            console.print(f"[green]✅ Utilisateur supprimé ({i + 1}/{len(users)}): [bold]{user['name']}[/bold][/green]")
                            deleted_users += 1
                            progress.update(task, advance=1)

                            # Pause entre les suppressions
                            if i < len(users) - 1:
                                console.print(f"[dim]⏱️  Pause de {delay}s...[/dim]")
                                time.sleep(delay)

                        except Exception as e:
                            console.print(f"[red]❌ Erreur suppression User {user['id']}: {e}[/red]")
                            progress.update(task, advance=1)
                            
                            # Pause même en cas d'erreur
                            if i < len(users) - 1:
                                console.print(f"[dim]⏱️  Pause après erreur ({delay}s)...[/dim]")
                                time.sleep(delay)

            console.print(f"[bold cyan]📊 Résultat Utilisateurs: [green]{deleted_users}/{len(users)} supprimés[/green][/bold cyan]")
            
        except Exception as e:
            console.print(f"[red]❌ Erreur lors de la récupération des utilisateurs: {e}[/red]")

        # Résumé final
        total_deleted = deleted_vms + deleted_users
        summary_table = Table(title="🎯 Résumé du nettoyage")
        summary_table.add_column("Type", style="cyan")
        summary_table.add_column("Supprimé", style="green")
        summary_table.add_column("Total", style="yellow")
        
        summary_table.add_row("VMs", str(deleted_vms), str(len(vms)))
        summary_table.add_row("Utilisateurs", str(deleted_users), str(len(users)))
        summary_table.add_row("**TOTAL**", f"[bold]{total_deleted}[/bold]", f"[bold]{len(vms) + len(users)}[/bold]")
        
        console.print(summary_table)
        console.print(Panel.fit(
            "[bold green]✅ NETTOYAGE TERMINÉ AVEC SUCCÈS ![/bold green]",
            border_style="green"
        ))

    except Exception as e:
        console.print(f"[bold red]❌ Erreur critique: {e}[/bold red]")
        raise typer.Exit(1)


def main():
    """Point d'entrée principal"""
    args = sys.argv[1:]

    # Paramètres par défaut
    simulate = True
    delay = 2.5

    # Parse arguments simples
    i = 0
    while i < len(args):
        arg = args[i]

        if arg in ("--real", "--confirm"):
            simulate = False
        elif arg == "--delay":
            # Récupérer la valeur du délai
            if i + 1 < len(args) and args[i + 1].replace(".", "").isdigit():
                delay = float(args[i + 1])
                i += 1  # Skip la valeur du délai
            else:
                print("❌ Erreur: --delay nécessite une valeur numérique")
                sys.exit(1)
        elif arg in ("--help", "-h"):
            print("Usage:")
            print("  python quick_cleanup.py                    # Mode simulation")
            print(
                "  python quick_cleanup.py --real             # Suppression réelle (délai 2.5s)"
            )
            print(
                "  python quick_cleanup.py --real --delay 3   # Suppression réelle avec délai personnalisé"
            )
            print("  python quick_cleanup.py --help             # Affiche cette aide")
            sys.exit(0)
        else:
            print(f"❌ Argument inconnu: {arg}")
            print("Utilisez --help pour voir l'aide")
            sys.exit(1)

        i += 1

    print(f"🔧 Configuration:")
    print(f"   Mode: {'Simulation' if simulate else 'Suppression réelle'}")
    print(f"   Délai entre opérations: {delay}s")
    print()

    quick_cleanup(simulate, delay)


if __name__ == "__main__":
    main()
