#!/usr/bin/env python3
"""
Script de nettoyage pour supprimer toutes les VMs et utilisateurs

⚠️  ATTENTION: Ce script supprime TOUTES les données de l'API !
Utilisez-le uniquement en environnement de test/development.
"""

import sys
import time
from typing import List, Dict, Any
from utils.api import ApiClient, create_authenticated_client
from utils.api.exceptions import (
    VMsFetchError, VMDeleteError, UsersFetchError, UserDeleteError
)
from utils.logging_config import get_logger

logger = get_logger(__name__)


class DataCleanup:
    """Gestionnaire de nettoyage des données via l'API"""
    
    def __init__(self, base_url: str = None, email: str = None, password: str = None):
        """
        Initialise le nettoyeur de données
        
        Args:
            base_url: URL de base de l'API
            email: Email pour l'authentification  
            password: Mot de passe pour l'authentification
        """
        self.client = create_authenticated_client(base_url, email, password)
        logger.info("DataCleanup initialisé", 
                   base_url=self.client.base_url,
                   authenticated=self.client.is_authenticated())
    
    def get_all_vms(self) -> List[Dict[str, Any]]:
        """Récupère toutes les VMs"""
        try:
            vms = self.client.vms.get()
            logger.info("VMs récupérées", count=len(vms))
            return vms
        except VMsFetchError as e:
            logger.error("Erreur lors de la récupération des VMs", error=str(e))
            raise
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Récupère tous les utilisateurs"""
        try:
            users = self.client.users.get()
            logger.info("Utilisateurs récupérés", count=len(users))
            return users
        except UsersFetchError as e:
            logger.error("Erreur lors de la récupération des utilisateurs", error=str(e))
            raise
    
    def delete_vm(self, vm_id: int, vm_name: str = None) -> bool:
        """
        Supprime une VM
        
        Args:
            vm_id: ID de la VM
            vm_name: Nom de la VM (pour le log)
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        try:
            result = self.client.vms.delete(vm_id)
            logger.info("VM supprimée avec succès", 
                       vm_id=vm_id, 
                       vm_name=vm_name,
                       result=result)
            return True
        except VMDeleteError as e:
            logger.error("Erreur lors de la suppression de la VM", 
                       vm_id=vm_id,
                       vm_name=vm_name,
                       error=str(e))
            return False
    
    def delete_user(self, user_id: int, user_name: str = None, user_email: str = None) -> bool:
        """
        Supprime un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            user_name: Nom de l'utilisateur (pour le log)
            user_email: Email de l'utilisateur (pour le log)
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        try:
            result = self.client.users.delete_user(user_id)
            logger.info("Utilisateur supprimé avec succès", 
                       user_id=user_id,
                       user_name=user_name,
                       user_email=user_email,
                       result=result)
            return True
        except UserDeleteError as e:
            logger.error("Erreur lors de la suppression de l'utilisateur", 
                       user_id=user_id,
                       user_name=user_name,
                       user_email=user_email,
                       error=str(e))
            return False
    
    def cleanup_all_vms(self, confirm: bool = False) -> Dict[str, Any]:
        """
        Supprime toutes les VMs
        
        Args:
            confirm: Si True, effectue la suppression. Si False, retourne juste les infos
            
        Returns:
            Dict avec stats de suppression
        """
        logger.info("🔍 Analyse des VMs à supprimer")
        vms = self.get_all_vms()
        
        stats = {
            "total_vms": len(vms),
            "deleted_vms": 0,
            "failed_deletions": 0,
            "vm_details": []
        }
        
        if not confirm:
            logger.info("📋 Mode simulation - aucune suppression effectuée")
            
        for vm in vms:
            vm_id = vm.get("id")
            vm_name = vm.get("name", "Sans nom")
            user_id = vm.get("user_id", "Inconnu")
            
            vm_info = {
                "id": vm_id,
                "name": vm_name,
                "user_id": user_id,
                "status": vm.get("status", "Inconnu")
            }
            stats["vm_details"].append(vm_info)
            
            logger.info("VM trouvée", **vm_info)
            
            if confirm:
                success = self.delete_vm(vm_id, vm_name)
                if success:
                    stats["deleted_vms"] += 1
                    time.sleep(0.1)  # Petite pause pour ne pas surcharger l'API
                else:
                    stats["failed_deletions"] += 1
        
        return stats
    
    def cleanup_all_users(self, confirm: bool = False) -> Dict[str, Any]:
        """
        Supprime tous les utilisateurs
        
        Args:
            confirm: Si True, effectue la suppression. Si False, retourne juste les infos
            
        Returns:
            Dict avec stats de suppression
        """
        logger.info("🔍 Analyse des utilisateurs à supprimer")
        users = self.get_all_users()
        
        stats = {
            "total_users": len(users),
            "deleted_users": 0,
            "failed_deletions": 0,
            "user_details": []
        }
        
        if not confirm:
            logger.info("📋 Mode simulation - aucune suppression effectuée")
            
        for user in users:
            user_id = user.get("id")
            user_name = user.get("name", "Sans nom")
            user_email = user.get("email", "Sans email")
            
            user_info = {
                "id": user_id,
                "name": user_name,
                "email": user_email,
                "created_at": user.get("created_at")
            }
            stats["user_details"].append(user_info)
            
            logger.info("Utilisateur trouvé", **user_info)
            
            if confirm:
                success = self.delete_user(user_id, user_name, user_email)
                if success:
                    stats["deleted_users"] += 1
                    time.sleep(0.1)  # Petite pause pour ne pas surcharger l'API
                else:
                    stats["failed_deletions"] += 1
        
        return stats
    
    def cleanup_everything(self, confirm: bool = False) -> Dict[str, Any]:
        """
        Supprime toutes les données (VMs puis utilisateurs)
        
        Args:
            confirm: Si True, effectue la suppression. Si False, retourne juste les infos
            
        Returns:
            Dict avec stats complètes de suppression
        """
        logger.info("🧹 Début du nettoyage complet des données", confirm=confirm)
        
        # D'abord supprimer les VMs (pour éviter les dépendances)
        logger.info("💻 Suppression des VMs...")
        vms_stats = self.cleanup_all_vms(confirm)
        
        time.sleep(1)  # Pause avant les utilisateurs
        
        # Ensuite supprimer les utilisateurs
        logger.info("👥 Suppression des utilisateurs...")
        users_stats = self.cleanup_all_users(confirm)
        
        # Statistiques globales
        total_stats = {
            "vms": vms_stats,
            "users": users_stats,
            "summary": {
                "total_items": vms_stats["total_vms"] + users_stats["total_users"],
                "deleted_items": vms_stats["deleted_vms"] + users_stats["deleted_users"],
                "failed_items": vms_stats["failed_deletions"] + users_stats["failed_deletions"],
                "success_rate": 0
            }
        }
        
        if total_stats["summary"]["total_items"] > 0:
            total_stats["summary"]["success_rate"] = (
                total_stats["summary"]["deleted_items"] / 
                total_stats["summary"]["total_items"] * 100
            )
        
        logger.info("✅ Nettoyage terminé", 
                   **total_stats["summary"])
        
        return total_stats


def print_stats(stats: Dict[str, Any]):
    """Affiche les statistiques de nettoyage de façon claire"""
    print("\n" + "="*60)
    print("📊 RÉSULTATS DU NETTOYAGE")
    print("="*60)
    
    # Résumé global
    summary = stats.get("summary", {})
    print(f"🎯 Résumé global:")
    print(f"   Total éléments: {summary.get('total_items', 0)}")
    print(f"   Supprimés: {summary.get('deleted_items', 0)}")
    print(f"   Échoués: {summary.get('failed_items', 0)}")
    print(f"   Taux de succès: {summary.get('success_rate', 0):.1f}%")
    
    # Détails VMs
    vms_stats = stats.get("vms", {})
    print(f"\n💻 VMs:")
    print(f"   Total: {vms_stats.get('total_vms', 0)}")
    print(f"   Supprimées: {vms_stats.get('deleted_vms', 0)}")
    print(f"   Échouées: {vms_stats.get('failed_deletions', 0)}")
    
    if vms_stats.get("vm_details"):
        print("   Détails:")
        for vm in vms_stats["vm_details"]:
            print(f"     • ID {vm.get('id')}: {vm.get('name')} (User: {vm.get('user_id')})")
    
    # Détails utilisateurs
    users_stats = stats.get("users", {})
    print(f"\n👥 Utilisateurs:")
    print(f"   Total: {users_stats.get('total_users', 0)}")
    print(f"   Supprimés: {users_stats.get('deleted_users', 0)}")
    print(f"   Échoués: {users_stats.get('failed_deletions', 0)}")
    
    if users_stats.get("user_details"):
        print("   Détails:")
        for user in users_stats["user_details"]:
            print(f"     • ID {user.get('id')}: {user.get('name')} ({user.get('email')})")


def main():
    """Fonction principale du script de nettoyage"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Script de nettoyage pour supprimer toutes les données de l'API",
        epilog="⚠️  ATTENTION: Ce script supprime TOUTES les données !"
    )
    
    parser.add_argument(
        "--base-url", 
        help="URL de base de l'API",
        default=None
    )
    parser.add_argument(
        "--email", 
        help="Email pour l'authentification"
    )
    parser.add_argument(
        "--password", 
        help="Mot de passe pour l'authentification"
    )
    parser.add_argument(
        "--simulate", 
        action="store_true",
        help="Mode simulation (n'affiche que ce qui serait supprimé)"
    )
    parser.add_argument(
        "--confirm", 
        action="store_true",
        help="Mode de confirmation - supprime réellement les données"
    )
    parser.add_argument(
        "--vms-only", 
        action="store_true",
        help="Supprime seulement les VMs"
    )
    parser.add_argument(
        "--users-only", 
        action="store_true",
        help="Supprime seulement les utilisateurs"
    )
    parser.add_argument(
        "--wait", 
        type=int, 
        default=5,
        help="Temps d'attente en secondes avant suppression (défaut: 5)"
    )
    
    args = parser.parse_args()
    
    # Vérifications de sécurité
    if args.confirm and not args.email:
        print("❌ ERREUR: L'email est requis pour confirmer la suppression réelle")
        print("   Utilisez --email votre@email.com --password votre-mot-de-passe")
        sys.exit(1)
    
    if not args.simulate and not args.confirm:
        print("⚠️  MODE SIMULATION activé par défaut")
        print("   Utilisez --confirm pour supprimer réellement les données")
        args.simulate = True
    
    print("🧹 SCRIPT DE NETTOYAGE DES DONNÉES")
    print("="*50)
    
    if args.confirm:
        print("⚠️  ATTENTION: Mode CONFIRMATION - suppression réelle !")
        for i in range(args.wait, 0, -1):
            print(f"   Suppression dans {i} secondes... (Ctrl+C pour annuler)")
            time.sleep(1)
        print("   🗑️  Suppression en cours...")
    else:
        print("📋 Mode SIMULATION - aucune donnée ne sera supprimée")
    
    try:
        # Initialiser le nettoyeur
        cleanup = DataCleanup(args.base_url, args.email, args.password)
        
        if args.vms_only:
            # Suppression des VMs seulement
            stats = cleanup.cleanup_all_vms(confirm=args.confirm)
            stats = {"vms": stats, "summary": stats}
            
        elif args.users_only:
            # Suppression des utilisateurs seulement
            stats = cleanup.cleanup_all_users(confirm=args.confirm)
            stats = {"users": stats, "summary": stats}
            
        else:
            # Suppression complète
            stats = cleanup.cleanup_everything(confirm=args.confirm)
        
        # Afficher les résultats
        print_stats(stats)
        
        if args.confirm:
            print("\n✅ Nettoyage terminé avec succès!")
        else:
            print("\n📋 Simulation terminée - utilisez --confirm pour supprimer réellement")
            
    except KeyboardInterrupt:
        print("\n⛔ Opération annulée par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        logger.error("Erreur critique lors du nettoyage", error=str(e))
        print(f"\n❌ Erreur critique: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
