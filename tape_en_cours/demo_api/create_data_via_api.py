#!/usr/bin/env python3
"""
Script pour créer des données via l'API en utilisant le générateur Faker.

Ce script utilise l'API unifiée pour créer des utilisateurs et des VMs
avec des données générées par Faker, permettant de peupler la base de données
avec des données réalistes.
"""

import typer
import time
from typing import Optional, List, Dict, Any
from pathlib import Path
import json
from datetime import datetime

from utils.api import ApiClient, create_authenticated_client
from utils.data_generator import DataGenerator, UserDataGenerator, VMDataGenerator
from utils.logging_config import get_logger
from utils.config import config

logger = get_logger(__name__)

app = typer.Typer(
    name="create-data-via-api",
    help="🚀 Créateur de données via API avec Faker",
    rich_markup_mode="markdown",
    add_completion=False,
    no_args_is_help=True,
)


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
    logger.info("Création d'utilisateurs via API", count=user_count, batch_size=batch_size)
    
    created_users = []
    created_count = 0
    
    for batch_start in range(0, user_count, batch_size):
        batch_end = min(batch_start + batch_size, user_count)
        batch_size_actual = batch_end - batch_start
        
        typer.echo(f"📝 Création du lot {batch_start//batch_size + 1}: utilisateurs {batch_start + 1}-{batch_end}")
        
        for i in range(batch_size_actual):
            try:
                # Générer les données utilisateur avec Faker
                user_data = UserDataGenerator.generate_user(created_count + 1)
                
                # Créer l'utilisateur via l'API
                created_user = api_client.users.create_user(
                    name=user_data["name"],
                    email=user_data["email"],
                    password="password123"  # Mot de passe par défaut
                )
                
                created_users.append(created_user)
                created_count += 1
                
                typer.echo(f"   ✅ {user_data['name']} ({user_data['email']})")
                
            except Exception as e:
                logger.error("Erreur lors de la création d'un utilisateur", error=str(e))
                typer.echo(f"   ❌ Erreur pour l'utilisateur {i + 1}: {e}")
        
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
    logger.info("Création de VMs via API", count=vm_count, available_users=len(user_ids))
    
    created_vms = []
    created_count = 0
    
    for batch_start in range(0, vm_count, batch_size):
        batch_end = min(batch_start + batch_size, vm_count)
        batch_size_actual = batch_end - batch_start
        
        typer.echo(f"🖥️ Création du lot {batch_start//batch_size + 1}: VMs {batch_start + 1}-{batch_end}")
        
        for i in range(batch_size_actual):
            try:
                # Générer les données VM avec Faker
                vm_data = VMDataGenerator.generate_vm(
                    user_id=user_ids[created_count % len(user_ids)], 
                    vm_id=created_count + 1
                )
                
                # Créer la VM via l'API
                created_vm = api_client.vms.create(
                    user_id=vm_data["user_id"],
                    name=vm_data["name"],
                    operating_system=vm_data["operating_system"],
                    cpu_cores=vm_data["cpu_cores"],
                    ram_gb=vm_data["ram_gb"],
                    disk_gb=vm_data["disk_gb"],
                    status=vm_data["status"]
                )
                
                created_vms.append(created_vm)
                created_count += 1
                
                typer.echo(f"   ✅ {vm_data['name']} ({vm_data['operating_system']}) - {vm_data['cpu_cores']}c/{vm_data['ram_gb']}GB")
                
            except Exception as e:
                logger.error("Erreur lors de la création d'une VM", error=str(e))
                typer.echo(f"   ❌ Erreur pour la VM {i + 1}: {e}")
        
        # Délai entre les lots pour éviter de surcharger l'API
        if batch_end < vm_count:
            time.sleep(delay_between_batches)
    
    logger.info("VMs créées avec succès", count=len(created_vms))
    return created_vms


@app.command()
def users(
    count: int = typer.Option(
        10, "--count", "-c", help="Nombre d'utilisateurs à créer", min=1, max=100
    ),
    batch_size: int = typer.Option(
        5, "--batch-size", "-b", help="Taille des lots", min=1, max=20
    ),
    delay: float = typer.Option(
        0.5, "--delay", "-d", help="Délai entre les lots (secondes)", min=0.1, max=5.0
    ),
    email: Optional[str] = typer.Option(
        None, "--email", "-e", help="Email pour l'authentification API"
    ),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", help="Mot de passe pour l'authentification API"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    👥 Créer des utilisateurs via l'API avec des données Faker
    
    Génère des utilisateurs réalistes avec Faker et les crée via l'API.
    
    Exemples:
    
    \b
    python create_data_via_api.py users --count 20
    python create_data_via_api.py users -c 50 --batch-size 10 --delay 1.0
    python create_data_via_api.py users --email admin@example.com --password secret
    """
    typer.echo(f"👥 Création de {count} utilisateurs via l'API...")
    
    try:
        # Créer le client API avec authentification
        api_client = create_authenticated_client(
            email=email,
            password=password
        )
        
        if not api_client.is_authenticated():
            typer.echo("❌ Impossible de s'authentifier avec l'API")
            typer.echo("💡 Utilisez --email et --password ou configurez les identifiants dans la config")
            raise typer.Exit(1)
        
        typer.echo(f"🔐 Authentifié avec succès sur {api_client.base_url}")
        
        # Créer les utilisateurs
        created_users = create_users_via_api(
            api_client=api_client,
            user_count=count,
            batch_size=batch_size,
            delay_between_batches=delay
        )
        
        # Statistiques
        typer.echo(f"\n✅ Création terminée !")
        typer.echo(f"📊 Statistiques:")
        typer.echo(f"   • Utilisateurs créés: {len(created_users)}")
        typer.echo(f"   • Taux de succès: {len(created_users)/count*100:.1f}%")
        
        if verbose and created_users:
            typer.echo(f"\n🔍 Aperçu des utilisateurs créés:")
            for i, user in enumerate(created_users[:5]):
                typer.echo(f"   {i + 1}. {user.get('name', 'N/A')} ({user.get('email', 'N/A')})")
            if len(created_users) > 5:
                typer.echo(f"   ... et {len(created_users) - 5} autres utilisateurs")
        
    except Exception as e:
        logger.error("Erreur lors de la création des utilisateurs", error=str(e))
        typer.echo(f"❌ Erreur lors de la création: {e}")
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
        0.5, "--delay", "-d", help="Délai entre les lots (secondes)", min=0.1, max=5.0
    ),
    email: Optional[str] = typer.Option(
        None, "--email", "-e", help="Email pour l'authentification API"
    ),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", help="Mot de passe pour l'authentification API"
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
    python create_data_via_api.py vms -c 100 --batch-size 10 --delay 1.0
    python create_data_via_api.py vms --email admin@example.com --password secret
    """
    typer.echo(f"🖥️ Création de {count} VMs via l'API...")
    
    try:
        # Créer le client API avec authentification
        api_client = create_authenticated_client(
            email=email,
            password=password
        )
        
        if not api_client.is_authenticated():
            typer.echo("❌ Impossible de s'authentifier avec l'API")
            typer.echo("💡 Utilisez --email et --password ou configurez les identifiants dans la config")
            raise typer.Exit(1)
        
        typer.echo(f"🔐 Authentifié avec succès sur {api_client.base_url}")
        
        # Récupérer les utilisateurs existants
        typer.echo("📋 Récupération des utilisateurs existants...")
        existing_users = api_client.users.get()
        
        if not existing_users:
            typer.echo("❌ Aucun utilisateur trouvé dans l'API")
            typer.echo("💡 Créez d'abord des utilisateurs avec la commande 'users'")
            raise typer.Exit(1)
        
        user_ids = [user["id"] for user in existing_users]
        typer.echo(f"👥 {len(user_ids)} utilisateurs disponibles pour l'association des VMs")
        
        # Créer les VMs
        created_vms = create_vms_via_api(
            api_client=api_client,
            vm_count=count,
            user_ids=user_ids,
            batch_size=batch_size,
            delay_between_batches=delay
        )
        
        # Statistiques
        typer.echo(f"\n✅ Création terminée !")
        typer.echo(f"📊 Statistiques:")
        typer.echo(f"   • VMs créées: {len(created_vms)}")
        typer.echo(f"   • Taux de succès: {len(created_vms)/count*100:.1f}%")
        
        if verbose and created_vms:
            typer.echo(f"\n🔍 Aperçu des VMs créées:")
            for i, vm in enumerate(created_vms[:5]):
                typer.echo(f"   {i + 1}. {vm.get('name', 'N/A')} ({vm.get('operating_system', 'N/A')})")
            if len(created_vms) > 5:
                typer.echo(f"   ... et {len(created_vms) - 5} autres VMs")
        
    except Exception as e:
        logger.error("Erreur lors de la création des VMs", error=str(e))
        typer.echo(f"❌ Erreur lors de la création: {e}")
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
        0.5, "--delay", "-d", help="Délai entre les lots (secondes)", min=0.1, max=5.0
    ),
    email: Optional[str] = typer.Option(
        None, "--email", "-e", help="Email pour l'authentification API"
    ),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", help="Mot de passe pour l'authentification API"
    ),
    output_file: Optional[str] = typer.Option(
        None, "--output", "-o", help="Fichier de sortie pour sauvegarder les données créées"
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
    python create_data_via_api.py full-dataset -u 30 -v 100 --output dataset.json
    python create_data_via_api.py full-dataset --email admin@example.com --password secret
    """
    typer.echo(f"🎯 Création d'un dataset complet: {user_count} utilisateurs + {vm_count} VMs")
    
    try:
        # Créer le client API avec authentification
        api_client = create_authenticated_client(
            email=email,
            password=password
        )
        
        if not api_client.is_authenticated():
            typer.echo("❌ Impossible de s'authentifier avec l'API")
            typer.echo("💡 Utilisez --email et --password ou configurez les identifiants dans la config")
            raise typer.Exit(1)
        
        typer.echo(f"🔐 Authentifié avec succès sur {api_client.base_url}")
        
        # Étape 1: Créer les utilisateurs
        typer.echo(f"\n👥 Étape 1/2: Création de {user_count} utilisateurs...")
        created_users = create_users_via_api(
            api_client=api_client,
            user_count=user_count,
            batch_size=batch_size,
            delay_between_batches=delay
        )
        
        # Étape 2: Créer les VMs
        typer.echo(f"\n🖥️ Étape 2/2: Création de {vm_count} VMs...")
        user_ids = [user["id"] for user in created_users]
        created_vms = create_vms_via_api(
            api_client=api_client,
            vm_count=vm_count,
            user_ids=user_ids,
            batch_size=batch_size,
            delay_between_batches=delay
        )
        
        # Statistiques finales
        typer.echo(f"\n✅ Dataset créé avec succès !")
        typer.echo(f"📊 Statistiques finales:")
        typer.echo(f"   • Utilisateurs créés: {len(created_users)}")
        typer.echo(f"   • VMs créées: {len(created_vms)}")
        typer.echo(f"   • Taux de succès utilisateurs: {len(created_users)/user_count*100:.1f}%")
        typer.echo(f"   • Taux de succès VMs: {len(created_vms)/vm_count*100:.1f}%")
        
        # Sauvegarder les données si demandé
        if output_file:
            dataset = {
                "created_at": datetime.now().isoformat(),
                "users": created_users,
                "vms": created_vms,
                "statistics": {
                    "total_users": len(created_users),
                    "total_vms": len(created_vms),
                    "user_success_rate": len(created_users)/user_count*100,
                    "vm_success_rate": len(created_vms)/vm_count*100,
                }
            }
            
            output_path = Path(output_file)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(dataset, f, indent=4, ensure_ascii=False, default=str)
            
            typer.echo(f"💾 Dataset sauvegardé: {output_path.absolute()}")
        
        if verbose:
            typer.echo(f"\n🔍 Aperçu des données créées:")
            typer.echo(f"👥 Utilisateurs (premiers 3):")
            for i, user in enumerate(created_users[:3]):
                typer.echo(f"   {i + 1}. {user.get('name', 'N/A')} ({user.get('email', 'N/A')})")
            
            typer.echo(f"🖥️ VMs (premiers 3):")
            for i, vm in enumerate(created_vms[:3]):
                typer.echo(f"   {i + 1}. {vm.get('name', 'N/A')} ({vm.get('operating_system', 'N/A')})")
        
    except Exception as e:
        logger.error("Erreur lors de la création du dataset", error=str(e))
        typer.echo(f"❌ Erreur lors de la création: {e}")
        raise typer.Exit(1)


@app.command()
def status(
    email: Optional[str] = typer.Option(
        None, "--email", "-e", help="Email pour l'authentification API"
    ),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", help="Mot de passe pour l'authentification API"
    ),
) -> None:
    """
    📊 Afficher le statut actuel de l'API
    
    Récupère et affiche les statistiques actuelles des utilisateurs et VMs.
    
    Exemples:
    
    \b
    python create_data_via_api.py status
    python create_data_via_api.py status --email admin@example.com --password secret
    """
    typer.echo("📊 Récupération du statut de l'API...")
    
    try:
        # Créer le client API avec authentification
        api_client = create_authenticated_client(
            email=email,
            password=password
        )
        
        if not api_client.is_authenticated():
            typer.echo("❌ Impossible de s'authentifier avec l'API")
            typer.echo("💡 Utilisez --email et --password ou configurez les identifiants dans la config")
            raise typer.Exit(1)
        
        typer.echo(f"🔐 Authentifié avec succès sur {api_client.base_url}")
        
        # Récupérer toutes les données
        typer.echo("📋 Récupération des données...")
        all_data = api_client.get_all_data()
        
        # Afficher les statistiques
        typer.echo(f"\n📊 Statut actuel de l'API:")
        typer.echo(f"   • URL de l'API: {api_client.base_url}")
        typer.echo(f"   • Utilisateurs total: {all_data['total_users']}")
        typer.echo(f"   • VMs totales: {all_data['total_vms']}")
        typer.echo(f"   • Utilisateurs avec VMs: {all_data['users_with_vms']}")
        
        if all_data['total_users'] > 0:
            avg_vms = all_data['total_vms'] / all_data['total_users']
            typer.echo(f"   • Moyenne VMs/utilisateur: {avg_vms:.1f}")
        
    except Exception as e:
        logger.error("Erreur lors de la récupération du statut", error=str(e))
        typer.echo(f"❌ Erreur lors de la récupération: {e}")
        raise typer.Exit(1)


@app.command()
def version() -> None:
    """📋 Afficher la version du créateur de données"""
    typer.echo("create-data-via-api v1.0.0")
    typer.echo("Powered by Faker 🎲 + API unifiée 🚀")


def main():
    """Point d'entrée principal"""
    import sys

    # Gérer -h comme alias pour --help
    if "-h" in sys.argv and "--help" not in sys.argv:
        sys.argv[sys.argv.index("-h")] = "--help"

    try:
        app()
    except KeyboardInterrupt:
        typer.echo("\n⚠️  Création interrompue")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    main()
