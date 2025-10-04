#!/usr/bin/env python3
"""
Script utilitaire pour générer des données factices avec Faker.
Permet de générer des utilisateurs et VMs réalistes pour les tests et démonstrations.
"""

import json
import typer
import sys
from pathlib import Path
from typing import Optional

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_generator import DataGenerator
from utils.logging_config import get_logger

logger = get_logger(__name__)

app = typer.Typer(
    name="generate-data",
    help="🎲 Générateur de données factices avec Faker",
    rich_markup_mode="markdown",
    add_completion=False,
    no_args_is_help=True,
)


@app.command()
def users_with_vms(
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
    🎯 Générer des utilisateurs avec leurs VMs

    Génère un dataset complet d'utilisateurs français avec des VMs réalistes.
    Les données sont sauvegardées dans un fichier JSON.

    Exemples:

    \b
    python generate_data.py users-with-vms
    python generate_data.py users-with-vms --users 100 --max-vms 3
    python generate_data.py users-with-vms -u 25 -o mon_dataset.json --verbose
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
def vms_only(
    vm_count: int = typer.Option(
        100, "--vms", "-v", help="Nombre de VMs à générer", min=1, max=5000
    ),
    user_ids: str = typer.Option(
        "1,2,3,4,5",
        "--user-ids",
        "-u",
        help="IDs des utilisateurs (séparés par des virgules)",
    ),
    output_file: str = typer.Option(
        "vms_only.json", "--output", "-o", help="Fichier de sortie JSON"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    🖥️ Générer uniquement des VMs pour des utilisateurs existants

    Génère des VMs réalistes et les associe à des utilisateurs existants.

    Exemples:

    \b
    python generate_data.py vms-only
    python generate_data.py vms-only --vms 200 --user-ids "1,2,3,4,5,6,7,8,9,10"
    python generate_data.py vms-only -v 50 -u "1,2,3" -o mes_vms.json
    """
    try:
        # Parser les IDs des utilisateurs
        user_ids_list = [int(uid.strip()) for uid in user_ids.split(",") if uid.strip()]

        if not user_ids_list:
            typer.echo("❌ Aucun ID d'utilisateur valide fourni")
            raise typer.Exit(1)

        typer.echo(
            f"🖥️ Génération de {vm_count} VMs pour les utilisateurs {user_ids_list}..."
        )

        # Générer les VMs
        vms_data = DataGenerator.generate_vms_only(vm_count, user_ids_list)

        # Sauvegarder dans le fichier JSON
        output_path = Path(output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(vms_data, f, indent=4, ensure_ascii=False, default=str)

        # Statistiques par utilisateur
        user_vm_counts = {}
        for vm in vms_data:
            user_id = vm["user_id"]
            user_vm_counts[user_id] = user_vm_counts.get(user_id, 0) + 1

        typer.echo(f"✅ VMs générées avec succès !")
        typer.echo(f"📊 Statistiques:")
        typer.echo(f"   • VMs totales: {len(vms_data)}")
        typer.echo(f"   • Utilisateurs concernés: {len(user_vm_counts)}")
        typer.echo(f"📁 Fichier sauvegardé: {output_path.absolute()}")

        if verbose:
            typer.echo("\n🔍 Répartition par utilisateur:")
            for user_id, count in sorted(user_vm_counts.items()):
                typer.echo(f"   • Utilisateur {user_id}: {count} VMs")

    except ValueError as e:
        typer.echo(f"❌ Erreur dans les IDs d'utilisateurs: {e}")
        raise typer.Exit(1)
    except Exception as e:
        logger.error("Erreur lors de la génération des VMs", error=str(e))
        typer.echo(f"❌ Erreur lors de la génération: {e}")
        raise typer.Exit(1)


@app.command()
def preview(
    user_count: int = typer.Option(
        5, "--users", "-u", help="Nombre d'utilisateurs à prévisualiser", min=1, max=20
    ),
    max_vms: int = typer.Option(
        3, "--max-vms", help="Nombre maximum de VMs par utilisateur", min=0, max=10
    ),
) -> None:
    """
    👀 Prévisualiser les données générées sans les sauvegarder

    Affiche un aperçu des données qui seraient générées.

    Exemples:

    \b
    python generate_data.py preview
    python generate_data.py preview --users 10 --max-vms 2
    """
    typer.echo(
        f"👀 Prévisualisation de {user_count} utilisateurs avec 0-{max_vms} VMs chacun..."
    )

    try:
        # Générer les données pour prévisualisation
        users_data = DataGenerator.generate_users_with_vms(
            user_count=user_count, vm_per_user_range=(0, max_vms)
        )

        typer.echo(f"\n📋 Aperçu des données générées:")
        typer.echo("=" * 60)

        for i, user in enumerate(users_data, 1):
            typer.echo(f"\n👤 Utilisateur {i}:")
            typer.echo(f"   • Nom: {user['name']}")
            typer.echo(f"   • Email: {user['email']}")
            typer.echo(f"   • Créé le: {user['created_at']}")
            typer.echo(f"   • VMs: {len(user['vms'])}")

            if user["vms"]:
                typer.echo(f"   🖥️ VMs:")
                for j, vm in enumerate(user["vms"], 1):
                    typer.echo(f"      {j}. {vm['name']} ({vm['operating_system']})")
                    typer.echo(
                        f"         CPU: {vm['cpu_cores']} cœurs, RAM: {vm['ram_gb']}GB, Disque: {vm['disk_gb']}GB"
                    )
                    typer.echo(f"         Statut: {vm['status']}")

        total_vms = sum(len(user["vms"]) for user in users_data)
        typer.echo(f"\n📊 Résumé:")
        typer.echo(f"   • Utilisateurs: {len(users_data)}")
        typer.echo(f"   • VMs totales: {total_vms}")
        typer.echo(f"   • Moyenne VMs/utilisateur: {total_vms / len(users_data):.1f}")

    except Exception as e:
        logger.error("Erreur lors de la prévisualisation", error=str(e))
        typer.echo(f"❌ Erreur lors de la prévisualisation: {e}")
        raise typer.Exit(1)


@app.command()
def version() -> None:
    """📋 Afficher la version du générateur"""
    typer.echo("generate-data v1.0.0")
    typer.echo("Powered by Faker 🎲")


def main():
    """Point d'entrée principal"""
    import sys

    # Gérer -h comme alias pour --help
    if "-h" in sys.argv and "--help" not in sys.argv:
        sys.argv[sys.argv.index("-h")] = "--help"

    try:
        app()
    except KeyboardInterrupt:
        typer.echo("\n⚠️  Génération interrompue")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    main()
