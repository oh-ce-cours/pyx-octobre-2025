#!/usr/bin/env python3
"""
Script de nettoyage rapide et simple pour les VMs et utilisateurs

Usage simple:
    python quick_cleanup.py                    # Mode simulation
    python quick_cleanup.py --real             # Suppression réelle (délai par défaut 2.5s)
    python quick_cleanup.py --real --delay 3   # Suppression réelle avec délai personnalisé
"""

import sys
import time
from utils.api import create_authenticated_client
from utils.logging_config import get_logger

logger = get_logger(__name__)


def quick_cleanup(simulate: bool = True, delay: float = 2.5):
    """
    Nettoie rapidement toutes les données avec respect des limites de taux
    
    Args:
        simulate: Si True, mode simulation (aucune suppression réelle)
        delay: Délai en secondes entre les suppressions pour éviter les 429
    """

    if simulate:
        print("🧹 NETTOYAGE SIMULATION")
        print("=" * 30)
    else:
        print("🗑️  NETTOYAGE RÁEL!")
        print("=" * 30)

    try:
        # Connexion à l'API
        client = create_authenticated_client()
        print(f"✅ Connexion API établie: {client.base_url}")
        print(f"✅ Authentifié: {client.is_authenticated()}")

        # Récupérer les données actuelles
        print("\n📊 Données actuelles:")

        try:
            vms = client.vms.get()
            print(f"   💻 VMs: {len(vms)}")
            for vm in vms:
                print(f"      - ID {vm['id']}: {vm['name']} (User: {vm['user_id']})")
        except Exception as e:
            print(f"   ❌ Erreur VMs: {e}")

        try:
            users = client.users.get()
            print(f"   👥 Utilisateurs: {len(users)}")
            for user in users:
                print(f"      - ID {user['id']}: {user['name']} ({user['email']})")
        except Exception as e:
            print(f"   ❌ Erreur Utilisateurs: {e}")

        if simulate:
            print("\n📋 Mode simulation - aucune suppression réelle")
            return

        # Suppression réelle
        print(f"\n🗑️  Suppression en cours avec délai de {delay}s entre chaque opération...")

        # Supprimer les VMs d'abord
        try:
            vms = client.vms.get()
            deleted_vms = 0
            
            for i, vm in enumerate(vms):
                try:
                    client.vms.delete(vm["id"])
                    print(f"   ✅ VM supprimée ({i+1}/{len(vms)}): {vm['name']}")
                    deleted_vms += 1
                    
                    # Pause entre les suppressions pour éviter les 429
                    if i < len(vms) - 1:  # Pas de pause après la dernière suppression
                        print(f"   ⏱️  Pause de {delay}s avant la prochaine suppression...")
                        time.sleep(delay)
                        
                except Exception as e:
                    print(f"   ❌ Erreur suppression VM {vm['id']}: {e}")
                    # Pause même en cas d'erreur pour éviter d'aggraver les problèmes de rate limiting
                    if i < len(vms) - 1:
                        print(f"   ⏱️  Pause après erreur ({delay}s)...")
                        time.sleep(delay)

            print(f"📊 VMs supprimées: {deleted_vms}/{len(vms)}")
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des VMs: {e}")

        # Supprimer les utilisateurs ensuite
        try:
            users = client.users.get()
            deleted_users = 0
            
            print(f"\n👥 Suppression des utilisateurs avec délai de {delay}s...")
            
            for i, user in enumerate(users):
                try:
                    client.users.delete_user(user["id"])
                    print(f"   ✅ Utilisateur supprimé ({i+1}/{len(users)}): {user['name']}")
                    deleted_users += 1
                    
                    # Pause entre les suppressions pour éviter les 429
                    if i < len(users) - 1:  # Pas de pause après la dernière suppression
                        print(f"   ⏱️  Pause de {delay}s avant la prochaine suppression...")
                        time.sleep(delay)
                        
                except Exception as e:
                    print(f"   ❌ Erreur suppression User {user['id']}: {e}")
                    # Pause même en cas d'erreur pour éviter d'aggraver les problèmes de rate limiting
                    if i < len(users) - 1:
                        print(f"   ⏱️  Pause après erreur ({delay}s)...")
                        time.sleep(delay)

            print(f"📊 Utilisateurs supprimés: {deleted_users}/{len(users)}")
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des utilisateurs: {e}")

        print("\n✅ Nettoyage terminé!")

    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        sys.exit(1)


def main():
    """Point d'entrée principal"""
    args = sys.argv[1:]

    if "--real" in args or "--confirm" in args:
        simulate = False
    else:
        simulate = True

    quick_cleanup(simulate)


if __name__ == "__main__":
    main()
