#!/usr/bin/env python3
"""
Script de nettoyage rapide et simple pour les VMs et utilisateurs

Usage simple:
    python quick_cleanup.py           # Mode simulation
    python quick_cleanup.py --real    # Suppression réelle
"""

import sys
import time
from utils.api import create_authenticated_client
from utils.logging_config import get_logger

logger = get_logger(__name__)


def quick_cleanup(simulate: bool = True):
    """Nettoie rapidement toutes les données"""

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
        print("\n🗑️  Suppression en cours...")

        # Supprimer les VMs d'abord
        try:
            vms = client.vms.get()
            deleted_vms = 0
            for vm in vms:
                try:
                    client.vms.delete(vm["id"])
                    print(f"   ✅ VM supprimée: {vm['name']}")
                    deleted_vms += 1
                except Exception as e:
                    print(f"   ❌ Erreur suppression VM {vm['id']}: {e}")

            print(f"📊 VMs supprimées: {deleted_vms}/{len(vms)}")
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des VMs: {e}")

        # Supprimer les utilisateurs ensuite
        try:
            users = client.users.get()
            deleted_users = 0
            for user in users:
                try:
                    client.users.delete_user(user["id"])
                    print(f"   ✅ Utilisateur supprimé: {user['name']}")
                    deleted_users += 1
                except Exception as e:
                    print(f"   ❌ Erreur suppression User {user['id']}: {e}")

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
