#!/usr/bin/env python3
"""
Script de test pour démontrer les améliorations Rich dans create_data_via_api.py
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

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

console = Console()


def demo_rich_features():
    """Démontre les fonctionnalités Rich utilisées dans le script"""

    # En-tête
    console.print(
        Panel.fit(
            "[bold blue]🚀 Démonstration des améliorations Rich[/bold blue]\n"
            "[dim]Script create_data_via_api.py avec affichage amélioré[/dim]",
            border_style="blue",
        )
    )

    # Tableau de configuration
    config_table = Table(title="🔧 Configuration API")
    config_table.add_column("Paramètre", style="cyan")
    config_table.add_column("Valeur", style="magenta")

    config_table.add_row("Base URL", "http://localhost:8000")
    config_table.add_row("Authentifié", "✅ Oui")
    config_table.add_row("Mode", "Production")

    console.print(config_table)
    console.print()

    # Simulation de barre de progression
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Création de 10 utilisateurs...", total=10)

        for i in range(10):
            progress.update(task, advance=1)
            console.print(
                f"[green]✅ Utilisateur {i + 1} créé:[/green] [bold]Jean Dupont[/bold] [dim](jean.dupont@example.com)[/dim]"
            )

    # Statistiques finales
    stats_table = Table(title="📊 Résultat de la création")
    stats_table.add_column("Métrique", style="cyan")
    stats_table.add_column("Valeur", style="green")

    stats_table.add_row("Utilisateurs créés", "10")
    stats_table.add_row("Taux de succès", "100%")
    stats_table.add_row("Temps écoulé", "2.5s")

    console.print(stats_table)
    console.print()

    # Message de succès
    console.print(
        Panel.fit(
            "[bold green]✅ CRÉATION TERMINÉE AVEC SUCCÈS ![/bold green]",
            border_style="green",
        )
    )


if __name__ == "__main__":
    demo_rich_features()
