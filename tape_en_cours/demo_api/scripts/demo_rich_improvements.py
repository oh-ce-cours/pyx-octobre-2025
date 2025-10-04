#!/usr/bin/env python3
"""
Démonstration des améliorations Rich dans create_data_via_api.py
Montre les nouvelles fonctionnalités d'affichage sans nécessiter une connexion API
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)
import time

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

console = Console()

def show_old_vs_new_comparison():
    """Montre la différence entre l'ancien et le nouveau style d'affichage"""
    
    console.print("\n[bold red]🔴 ANCIEN STYLE (avec typer.echo):[/bold red]")
    console.print("👥 Création de 10 utilisateurs via l'API...")
    console.print("🔐 Authentifié avec succès sur http://localhost:8000")
    console.print("📝 Création du lot 1: utilisateurs 1-5")
    console.print("   ✅ Jean Dupont (jean.dupont@example.com)")
    console.print("   ✅ Marie Martin (marie.martin@example.com)")
    console.print("✅ Création terminée !")
    console.print("📊 Statistiques:")
    console.print("   • Utilisateurs créés: 10")
    console.print("   • Taux de succès: 100%")
    
    console.print("\n[bold green]🟢 NOUVEAU STYLE (avec Rich):[/bold green]")

    # Nouveau style avec Rich
    console.print(
        Panel.fit(
            "[bold blue]👥 Création d'utilisateurs via l'API[/bold blue]\n"
            "[dim]Génération de 10 utilisateurs avec Faker[/dim]",
            border_style="blue",
        )
    )
    
    console.print(
        f"[bold green]🔐 Authentifié avec succès sur http://localhost:8000[/bold green]"
    )
    console.print()
    
    # Configuration API
    config_table = Table(title="🔗 Configuration API")
    config_table.add_column("Paramètre", style="cyan")
    config_table.add_column("Valeur", style="magenta")
    
    config_table.add_row("Base URL", "http://localhost:8000")
    config_table.add_row("Authentifié", "✅ Oui")
    
    console.print(config_table)
    console.print()
    
    # Configuration des opérations
    operation_table = Table(title="🔧 Configuration - Utilisateurs")
    operation_table.add_column("Paramètre", style="cyan")
    operation_table.add_column("Valeur", style="magenta")
    
    operation_table.add_row("Nombre total", "10")
    operation_table.add_row("Taille des lots", "5")
    operation_table.add_row("Délai entre lots", "0.5s")
    
    console.print(operation_table)
    console.print()
    
    # Barre de progression
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Création de 10 utilisateurs...", total=10)
        
        users = [
            ("Jean Dupont", "jean.dupont@example.com"),
            ("Marie Martin", "marie.martin@example.com"),
            ("Pierre Bernard", "pierre.bernard@example.com"),
            ("Sophie Leroy", "sophie.leroy@example.com"),
            ("Luc Moreau", "luc.moreau@example.com"),
            ("Claire Petit", "claire.petit@example.com"),
            ("Antoine Dubois", "antoine.dubois@example.com"),
            ("Julie Robert", "julie.robert@example.com"),
            ("Thomas Richard", # Continuation de la ligne suivante
             "thomas.richard@example.com"),
            ("Camille Simon", "camille.simon@example.com"),
        ]
        
        for i, (name, email) in enumerate(users):
            time.sleep(0.1)  # Simulation du temps de création
            progress.update(task, advance=1)
            console.print(f"[green]✅ Utilisateur créé:[/green] [bold]{name}[/bold] [dim]({email})[/dim]")
    
    # Statistiques finales
    stats_table = Table(title="📊 Résultat de la création")
    stats_table.add_column("Métrique", style="cyan")
    stats_table.add_column("Valeur", style="green")
    
    stats_table.add_row("Utilisateurs créés", "10")
    stats_table.add_row("Taux de succès", "100%")
    
    console.print(stats_table)
    console.print()
    
    # Message de succès
    console.print(
        Panel.fit(
            "[bold green]✅ CRÉATION TERMINÉE AVEC SUCCÈS ![/bold green]",
            border_style="green",
        )
    )

def show_improvements_summary():
    """Montre un résumé des améliorations apportées"""
    
    console.print("\n[bold cyan]📋 RÉSUMÉ DES AMÉLIORATIONS RICH:[/bold cyan]\n")
    
    improvements_table = Table(title="✨ Fonctionnalités ajoutées")
    improvements_table.add_column("Composant", style="cyan")
    improvements_table.add_column("Description", style="green")
    improvements_table.add_column("Avantage", style="yellow")
    
    improvements_table.add_row(
        "🎨 Panneaux colorés",
        "En-têtes et messages encadrés avec couleurs",
        "Meilleure lisibilité des sections"
    )
    improvements_table.add_row(
        "📊 Tableaux structurés",
        "Configuration et statistiques en tableaux",
        "Information organisée et claire"
    )
    improvements_table.add_row(
        "⏳ Barres de progression",
        "Suivi en temps réel des opérations",
        "Feedback visuel pendant l'exécution"
    )
    improvements_table.add_row(
        "🎯 Messages contextuels",
        "Messages de succès/erreur colorés",
        "Identification rapide des résultats"
    )
    improvements_table.add_row(
        "🔄 Séparation logique",
        "Code organisé : affichage ↔ données",
        "Maintenabilité et lisibilité"
    )
    
    console.print(improvements_table)
    console.print()
    
    console.print(
        Panel.fit(
            "[bold green]🚀 Le script create_data_via_api.py utilise maintenant Rich ![/bold green]\n"
            "[dim]Séparation claire entre logique métier et représentation visuelle[/dim]",
            border_style="green",
        )
    )

if __name__ == "__main__":
    console.print(
        Panel.fit(
            "[bold blue]🧪 DÉMONSTRATION DES AMÉLIORATIONS RICH[/bold blue]\n"
            "[dim]Script create_data_via_api.py - Avant vs Après[/dim]",
            border_style="blue",
        )
    )
    
    show_old_vs_new_comparison()
    show_improvements_summary()
