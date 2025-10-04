#!/usr/bin/env python3
"""
Script de démonstration des améliorations de la barre de progression
pour quick_cleanup.py
"""

import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn, MofNCompleteColumn
from rich.panel import Panel

console = Console()

def demo_progress_bar():
    """Démonstration de la nouvelle barre de progression"""
    
    console.print(
        Panel.fit(
            "[bold cyan]🚀 DÉMONSTRATION DE LA BARRE DE PROGRESSION[/bold cyan]\n"
            "Simulation du processus de suppression avec délais",
            border_style="cyan",
        )
    )
    console.print()
    
    # Simulation de données
    vms = [
        {"id": 1, "name": "VM-Production-01"},
        {"id": 2, "name": "VM-Test-02"},
        {"id": 3, "name": "VM-Dev-03"},
    ]
    
    users = [
        {"id": 1, "name": "Alice Martin", "email": "alice@example.com"},
        {"id": 2, "name": "Bob Dupont", "email": "bob@example.com"},
    ]
    
    total_items = len(vms) + len(users)
    delay = 1.0  # Délai réduit pour la démo
    
    # Barre de progression globale
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
        console=console,
        expand=True,
    ) as global_progress:
        global_task = global_progress.add_task(
            "Nettoyage global", total=total_items
        )
        
        # Simulation suppression VMs
        console.print("[bold red]🗑️ Suppression des VMs...[/bold red]")
        estimated_time = len(vms) * delay + (len(vms) - 1) * delay
        console.print(f"[dim]⏱️ Temps estimé: ~{estimated_time:.1f}s[/dim]")
        console.print()
        
        for i, vm in enumerate(vms):
            global_progress.update(
                global_task, 
                description=f"Suppression VM: {vm['name']}",
                advance=0
            )
            
            # Simulation de la suppression
            time.sleep(0.5)
            console.print(f"[green]✅ VM supprimée: [bold]{vm['name']}[/bold][/green]")
            
            global_progress.update(global_task, advance=1)
            
            if i < len(vms) - 1:
                global_progress.update(
                    global_task, 
                    description=f"Pause {delay}s avant le prochain VM..."
                )
                time.sleep(delay)
        
        console.print(f"[bold cyan]📊 VMs supprimées: [green]{len(vms)}/{len(vms)}[/green][/bold cyan]")
        console.print()
        
        # Simulation suppression utilisateurs
        console.print("[bold red]🗑️ Suppression des utilisateurs...[/bold red]")
        estimated_time = len(users) * delay + (len(users) - 1) * delay
        console.print(f"[dim]⏱️ Temps estimé: ~{estimated_time:.1f}s[/dim]")
        console.print()
        
        for i, user in enumerate(users):
            global_progress.update(
                global_task, 
                description=f"Suppression utilisateur: {user['name']}",
                advance=0
            )
            
            # Simulation de la suppression
            time.sleep(0.5)
            console.print(f"[green]✅ Utilisateur supprimé: [bold]{user['name']}[/bold][/green]")
            
            global_progress.update(global_task, advance=1)
            
            if i < len(users) - 1:
                global_progress.update(
                    global_task, 
                    description=f"Pause {delay}s avant le prochain utilisateur..."
                )
                time.sleep(delay)
        
        console.print(f"[bold cyan]📊 Utilisateurs supprimés: [green]{len(users)}/{len(users)}[/green][/bold cyan]")
    
    # Résumé final
    console.print()
    console.print(
        Panel.fit(
            "[bold green]✅ NETTOYAGE TERMINÉ AVEC SUCCÈS ![/bold green]\n"
            f"Total: [bold]{total_items}[/bold] éléments supprimés",
            border_style="green",
        )
    )

if __name__ == "__main__":
    demo_progress_bar()
