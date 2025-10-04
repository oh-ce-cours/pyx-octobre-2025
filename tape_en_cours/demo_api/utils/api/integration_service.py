"""
Service d'intégration pour créer des utilisateurs et VMs via l'API avec des données Faker.
Permet la synchronisation entre les données générées et l'API externe.
"""

from typing import Dict, Any, List, Optional, Tuple
from utils.api.api_client import APIClient
from utils.data_generator import DataGenerator, UserDataGenerator, VMDataGenerator
from utils.logging_config import get_logger
from utils.config import config

logger = get_logger(__name__)


class APIIntegrationService:
    """Service d'intégration pour synchroniser les données Faker avec l'API externe."""
    
    def __init__(self, api_client: APIClient):
        """
        Initialise le service d'intégration.
        
        Args:
            api_client: Client API configuré
        """
        self.api = api_client
        self.created_users: Dict[int, Dict[str, Any]] = {}  # Cache des utilisateurs créés
        self.created_vms: Dict[int, Dict[str, Any]] = {}    # Cache des VMs créées
        
        logger.info("Service d'intégration API initialisé")
    
    def authenticate_admin(self, email: str = None, password: str = None) -> str:
        """
        S'authentifie avec le compte administrateur par défaut ou fourni.
        
        Args:
            email: Email de l'admin (optionnel)
            password: Mot de passe de l'admin (optionnel)
            
        Returns:
            Token d'authentification
        """
        if not email or not password:
            # Utiliser les credentials par défaut depuis la config
            email = getattr(config, 'ADMIN_EMAIL', 'admin@demo-api.com')
            password = getattr(config, 'ADMIN_PASSWORD', 'admin123')
        
        logger.info("Authentification administrateur", email=email)
        
        try:
            token = self.api.authenticate(email, password, signup=False)
            logger.info("Administrateur authentifié avec succès")
            return token
        except Exception as e:
            logger.warning("Échec de l'authentification admin, tentative de signup", error=str(e))
            token = self.api.authenticate(email, password, signup=True)
            logger.info("Administrateur créé avec succès")
            return token
    
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
                api_user = self.api.create_user(fake_user)
                
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
                # Sélectionner un utilisateur aléatoire
                user_id = target_user_ids[i % len(target_user_ids)]
                
                # Générer les données VM avec Faker
                fake_vm = VMDataGenerator.generate_vm(user_id, i)
                
                # Créer la VM via l'API
                api_vm = self.api.create_vm(fake_vm)
                
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
            user_count: Nombre d'utilisateurs à créer
            vm_per_user_range: Range (min, max) de VMs par utilisateur
            
        Returns:
            Statistiques de création
        """
        logger.info(
            "Création d'un dataset complet via l'API",
            users=user_count,
            vms_range=vm_per_user_range
        )
        
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
                        self.api.attach_vm_to_user(vm.get('id'), user_id)
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
    
    def sync_with_existing_data(self, existing_users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synchronise des données existantes avec l'API.
        
        Args:
            existing_users: Liste des utilisateurs existants avec leurs VMs
            
        Returns:
            Statistiques de synchronisation
        """
        logger.info("Synchronisation des données existantes avec l'API", users_count=len(existing_users))
        
        synced_users = 0
        synced_vms = 0
        failed_syncs = 0
        
        for user_data in existing_users:
            try:
                # Créer l'utilisateur s'il n'existe pas
                user_response = self.api.create_user(user_data)
                synced_users += 1
                
                # Créer ses VMs
                for vm_data in user_data.get('vms', []):
                    try:
                        vm_data['user_id'] = user_response.get('id')
                        vm_response = self.api.create_vm(vm_data)
                        synced_vms += 1
                    except Exception as e:
                        logger.warning(f"Échec de synchronisation de la VM", vm_name=vm_data.get('name'), error=str(e))
                        failed_syncs += 1
                        
            except Exception as e:
                logger.warning(f"Échec de synchronisation de l'utilisateur", user_name=user_data.get('name'), error=str(e))
                failed_syncs += 1
        
        stats = {
            'users_synced': synced_users,
            'vms_synced': synced_vms,
            'failed_syncs': failed_syncs,
            'success_rate': (synced_users + synced_vms) / max(1, len(existing_users) + sum(len(u.get('vms', [])) for u in existing_users)) * 100
        }
        
        logger.info("Synchronisation terminée", stats=stats)
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
            api_users = self.api.get_users()
            api_vms = self.api.get_vms()
            
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
    
    def cleanup_dataset(self) -> Dict[str, int]:
        """
        Nettoie tous les enregistrements créés via l'API.
        
        Returns:
            Statistiques de nettoyage
        """
        logger.warning("Nettoyage du dataset créé via l'API")
        
        deleted_vms = 0
        deleted_users = 0
        
        # Supprimer toutes les VMs
        for vm_id in self.created_vms.keys():
            try:
                self.api.delete_vm(vm_id)
                deleted_vms += 1
            except Exception as e:
                logger.warning(f"Échec de suppression de la VM {vm_id}", error=str(e))
        
        # Supprimer tous les utilisateurs
        for user_id in self.created_users.keys():
            try:
                self.api.delete_user(user_id)
                deleted_users += 1
            except Exception as e:
                logger.warning(f"Échec de suppression de l'utilisateur {user_id}", error=str(e))
        
        # Vider les caches
        self.created_users.clear()
        self.created_vms.clear()
        
        logger.info("Nettoyage terminé", deleted_users=deleted_users, deleted_vms=deleted_vms)
        return {
            'deleted_users': deleted_users,
            'deleted_vms': deleted_vms,
            'total_deleted': deleted_users + deleted_vms
        }
