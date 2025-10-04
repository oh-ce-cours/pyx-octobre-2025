#!/usr/bin/env python3
"""
Service d'intégration pour utiliser l'API externe avec les données Faker.
Permet de créer des utilisateurs et des VMs directement via l'API avec des données réalistes.
"""

import json
import typer
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from utils.api.user import create_user, get_users, update_user, delete_user
from utils.api.vm import create_vm, get_vms, update_vm, delete_vm, attach_vm_to_user, stop_vm
from utils.api.auth import Auth
from utils.data_generator import DataGenerator, UserDataGenerator, VMDataGenerator
from utils.logging_config import get_logger
from utils.config import config

logger = get_logger(__name__)

class APIIntegrationService:
    """Service d'intégration pour synchroniser les données Faker avec l'API externe."""
    
    def __init__(self, base_url: str, admin_email: str = None, admin_password: str = None):
        """
        Initialise le service d'intégration.
        
        Args:
            base_url: URL de base de l'API
            admin_email: Email de l'administrateur (optionnel)
            admin_password: Mot de passe de l'administrateur (optionnel)
        """
        self.base_url = base_url
        self.auth = Auth(base_url)
        self.token: Optional[str] = None
        self.admin_email = admin_email or getattr(config, 'ADMIN_EMAIL', 'admin@demo-api.com')
        self.admin_password = admin_password or getattr(config, 'ADMIN_PASSWORD', 'admin123')
        
        # Cache des données créées
        self.created_users: Dict[int, Dict[str, Any]] = {}
        self.created_vms: Dict[int, Dict[str, Any]] = {}
        
        logger.info("Service d'intégration API initialisé", base_url=base_url)
    
    def authenticate_admin(self) -> str:
        """
        S'authentifie avec le compte administrateur.
        
        Returns:
            Token d'authentification
        """
        logger.info("Authentification administrateur", email=self.admin_email)
        
        try:
            # Essayer de se connecter d'abord
            self.token = self.auth.login_user(self.admin_email, self.admin_password)
            logger.info("Administrateur authentifié avec succès")
        except Exception as e:
            logger.warning("Échec de l'authentification admin, tentative de création", error=str(e))
            try:
                # Créer l'administrateur s'il n'existe pas
                self.token = self.auth.create_user(self.admin_email.split('@')[0], self.admin_email, self.admin_password)
                logger.info("Administrateur créé avec succès")
            except Exception as create_error:
                logger.error("Impossible de créer ou d'authentifier l'administrateur", error=str(create_error))
                raise
        
        return self.token
    
    def create_user_batch(self, user_count: int) -> List[Dict[str, Any]]:
        """
        Crée un batch d'utilisateurs via l'API avec des données Faker.
        
        Args:
            user_count: Nombre d'utilisateurs à créer
            
        Returns:
            Liste des utilisateurs créés
        """
        logger.info("Création d'un batch d'utilisateurs", count=user_count)
        
        created_users = []
        failed_creations = []
        
        for i in range(1, user_count + 1):
            try:
                # Générer les données utilisateur avec Faker
                fake_user = UserDataGenerator.generate_user(i)
                
                # Créer l'utilisateur via l'API
                api_user = create_user(self.base_url, self.token, fake_user['name'], fake_user['email'])
                
                # Mettre en cache
                self.created_users[api_user.get('id', i)] = api_user
                created_users.append(api_user)
                
                logger.debug(
                    "Utilisateur créé avec succès",
                    user_id=api_user.get('id'),
                    name=fake_user['name'],
                    email=fake_user['email']
                )
                
            except Exception as e:
                logger.error(f"Échec de création de l'utilisateur {i}", error=str(e))
                failed_creations.append(fake_user)
        
        logger.info(
            "Batch d'utilisateurs terminé",
            created=len(created_users),
            failed=len(failed_creations)
        )
        
        return created_users
    
    def create_vm_batch(self, vm_count: int, target_user_ids: List[int] = None) -> List[Dict[str, Any]]:
        """
        Crée un batch de VMs via l'API avec des données Faker.
        
        Args:
            vm_count: Nombre de VMs à créer
            target_user_ids: IDs des utilisateurs cibles (optionnel)
            
        Returns:
            Liste des VMs créées
        """
        logger.info("Création d'un batch de VMs", count=vm_count)
        
        # Si aucun utilisateur spécifié, utiliser ceux créés précédemment
        if not target_user_ids:
            target_user_ids = list(self.created_users.keys())
        
        if not target_user_ids:
            logger.error("Aucun utilisateur disponible pour la création de VMs")
            return []
        
        created_vms = []
        failed_creations = []
        
        for i in range(1, vm_count + 1):
            try:
                # Sélectionner un utilisateur Par modulo pour distribuer équitablement
                user_id = target_user_ids[i % len(target_user_ids)]
                
                # Générer les données VM avec Faker
                fake_vm = VMDataGenerator.generate_vm(user_id, i)
                
                # Créer la VM via l'API
                api_vm = create_vm(
                    self.token,
                    self.base_url,
                    fake_vm['user_id'],
                    fake_vm['name'],
                    fake_vm['operating_system'],
                    fake_vm['cpu_cores'],
                    fake_vm['ram_gb'],
                    fake_vm['disk_gb'],
                    fake_vm['status']
                )
                
                # Mettre en cache
                self.created_vms[api_vm.get('id', i)] = api_vm
                created_vms.append(api_vm)
                
                logger.debug(
                    "VM créée avec succès",
                    vm_id=api_vm.get('id'),
                    name=fake_vm['name'],
                    user_id=user_id
                )
                
            except Exception as e:
                logger.error(f"Échec de création de la VM {i}", error=str(e))
                failed_creations.append(fake_vm)
        
        logger.info(
            "Batch de VMs terminé",
            created=len(created_vms),
            failed=len(failed_creations)
        )
        
        return created_vms
    
    def create_full_dataset(self, user_count: int, vm_per_user_range: Tuple[int, int]) -> Dict[str, Any]:
        """
        Crée un dataset complet via l'API (utilisateurs + VMs).
        
        Args:
            user_count: Nombre de utilisateurs à créer
            vm_per_user_range: Range (min, max) de VMs par utilisateur
            
        Returns:
            Statistiques de création
        """
        logger.info(
            "Création d'un dataset complet via l'API",
            users=user_count,
            vms_range=vm_per_user_range
        )
        
        # S'authentifier si nécessaire
        if not self.token:
            self.authenticate_admin()
        
        # Créer les utilisateurs
        users = self.create_user_batch(user_count)
        user_ids = [u.get('id') for u in users if u.get('id')]
        
        # Créer les VMs pour chaque utilisateur
        total_vms = 0
        all_vms = []
        
        for user in users:
            user_id = user.get('id')
            if not user_id:
                continue
            
            # Nombre de VMs aléatoire pour cet utilisateur
            import random
            vm_count = random.randint(vm_per_user_range[0], vm_per_user_range[1])
            
            if vm_count > 0:
                vms = self.create_vm_batch(vm_count, [user_id])
                all_vms.extend(vms)
                total_vms += len(vms)
                
                # Associer les VMs à l'utilisateur si nécessaire
                for vm in vms:
                    try:
                        attach_vm_to_user(self.base_url, self.token, vm.get('id'), user_id)
                    except Exception as e:
                        logger.warning(
                            "Échec de l'association VM-utilisateur",
                            vm_id=vm.get('id'),
                            user_id=user_id,
                            error=str(e)
                        )
        
        stats = {
            'users_created': len(users),
            'vms_created': total_vms,
            'total_records': len(users) + total_vms,
            'users_with_vms': len([u for u in users if any(vm.get('user_id') == u.get('id') for vm in all_vms)])
        }
        
        logger.info("Dataset complet créé avec succès", stats=stats)
        return stats
    
    def export_dataset(self) -> Dict[str, Any]:
        """
        Exporte le dataset créé via l'API vers le format JSON local.
        
        Returns:
            Dataset au format JSON
        """
        logger.info("Export du dataset créé via l'API")
        
        # Récupérer les utilisateurs depuis l'API
        try:
            api_users = get_users(self.base_url)
            api_vms = get_vms(self.base_url)
            
            # Reformater au format attendu
            dataset = []
            for user in api_users:
                user_vms = [vm for vm in api_vms if vm.get('user_id') == user.get('id')]
                
                user_record = {
                    'id': user.get('id'),
                    'name': user.get('name'),
                    'email': user.get('email'),
                    'created_at': user.get('created_at'),
                    'vms': user_vms
                }
                dataset.append(user_record)
            
            logger.info("Dataset exporté avec succès", users_count=len(dataset), vms_count=len(api_vms))
            return {
                'dataset': dataset,
                'stats': {
                    'total_users': len(dataset),
                    'total_vms': len(api_vms),
                    'users_with_vms': len([u for u in dataset if u['vms']])
                }
            }
            
        except Exception as e:
            logger.error("Échec de l'export du dataset", error=str(e))
            raise


# CLI pour utiliser le service d'intégration
app = typer.Typer(
    name="api-integration",
    help="🌐 Service d'intégration API avec Faker",
    rich_markup_mode="markdown",
    add_completion=False,
    no_args_is_help=True,
)


@app.command()
def create_dataset(
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
        None, "--admin-password", "-p", help="Mot de passe de l'administrateur", hide_input=True
    ),
    export_file: str = typer.Option(
        "api_dataset.json", "--export", "-e", help="Fichier d'export du dataset"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Mode verbeux"),
) -> None:
    """
    🎯 Créer un dataset complet via l'API avec des données Faker
    
    Crée des utilisateurs et des VMs directement via l'API avec des données réalistes
    générées par Faker.
    
    Exemples:
    
    \b
    python api_data_manager.py create-dataset --base-url "https://api.example.com"
    python api_data_manager.py create-dataset -u "https://api.example.com" --users 50 --max-vms 5
    """
    if min_vms > max_vms:
        typer.echo("❌ Le nombre minimum de VMs ne peut pas être supérieur au maximum")
        raise typer.Exit(1)
    
    typer.echo(f"🌐 Création d'un dataset via l'API {base_url}...")
    typer.echo(f"   • Utilisateurs: {user_count}")
    typer.echo(f"   • VMs par utilisateur: {min_vms}-{max_vms}")
    
    try:
        # Initialiser le service
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
                json.dump(export_data['dataset'], f, indent=4, ensure_ascii=False, default=str)
            
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
        logger.error("Erreur lors de la création du dataset", error=str(e))
        typer.echo(f"❌ Erreur lors de la création du dataset: {e}")
        raise typer.Exit(1)


def main():
    """Point d'entrée principal"""
    import sys
    
    try:
        app()
    except KeyboardInterrupt:
        typer.echo("\n⚠️  Création interrompue")
    except Exception as e:
        typer.echo(f"❌ Erreur: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    main()
