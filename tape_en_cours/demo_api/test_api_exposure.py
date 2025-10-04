#!/usr/bin/env python3
"""
Script de test pour vérifier que toutes les méthodes de l'API sont exposées dans ApiClient
"""

import sys
import inspect
from utils.api import ApiClient, UsersAPI, VMsAPI, AuthAPI

def get_methods(cls):
    """Récupère toutes les méthodes publiques d'une classe"""
    methods = []
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith('_'):
            methods.append(name)
    return sorted(methods)

def test_api_exposure():
    """Teste que toutes les méthodes sont bien exposées"""
    print("🔍 Vérification de l'exposition des méthodes dans ApiClient\n")
    
    # Méthodes attendues pour chaque interface
    users_expected = ['get', 'add_vms_to_users', 'get_user', 'create_user', 'update_user', 'delete_user', 'create_vm']
    vms_expected = ['get', 'create', 'get_vm', 'update', 'delete', 'attach_to_user', 'stop']
    auth_expected = ['login', 'create_user', 'get_user_info']
    client_expected = ['login', 'create_user', 'get_user_info', 'is_authenticated', 'set_token', 'clear_token', 'get_all_data', 'get_user_data', 'get_vm_data']
    
    # Méthodes disponibles
    users_methods = get_methods(UsersAPI)
    vms_methods = get_methods(VMsAPI)
    auth_methods = get_methods(AuthAPI)
    client_methods = get_methods(ApiClient)
    
    print("📋 Méthodes UsersAPI:")
    print(f"   Attendues: {users_expected}")
    print(f"   Disponibles: {users_methods}")
    missing_users = set(users_expected) - set(users_methods)
    extra_users = set(users_methods) - set(users_expected)
    if missing_users:
        print(f"   ❌ Manquantes: {missing_users}")
    if extra_users:
        print(f"   ➕ Supplémentaires: {extra_users}")
    if not missing_users and not extra_users:
        print("   ✅ Toutes les méthodes sont présentes")
    print()
    
    print("📋 Méthodes VMsAPI:")
    print(f"   Attendues: {vms_expected}")
    print(f"   Disponibles: {vms_methods}")
    missing_vms = set(vms_expected) - set(vms_methods)
    extra_vms = set(vms_methods) - set(vms_expected)
    if missing_vms:
        print(f"   ❌ Manquantes: {missing_vms}")
    if extra_vms:
        print(f"   ➕ Supplémentaires: {extra_vms}")
    if not missing_vms and not extra_vms:
        print("   ✅ Toutes les méthodes sont présentes")
    print()
    
    print("📋 Méthodes AuthAPI:")
    print(f"   Attendues: {auth_expected}")
    print(f"   Disponibles: {auth_methods}")
    missing_auth = set(auth_expected) - set(auth_methods)
    extra_auth = set(auth_methods) - set(auth_expected)
    if missing_auth:
        print(f"   ❌ Manquantes: {missing_auth}")
    if extra_auth:
        print(f"   ➕ Supplémentaires: {extra_auth}")
    if not missing_auth and not extra_auth:
        print("   ✅ Toutes les méthodes sont présentes")
    print()
    
    print("📋 Méthodes ApiClient (directes):")
    print(f"   Attendues: {client_expected}")
    print(f"   Disponibles: {client_methods}")
    missing_client = set(client_expected) - set(client_methods)
    extra_client = set(client_methods) - set(client_expected)
    if missing_client:
        print(f"   ❌ Manquantes: {missing_client}")
    if extra_client:
        print(f"   ➕ Supplémentaires: {extra_client}")
    if not missing_client and not extra_client:
        print("   ✅ Toutes les méthodes sont présentes")
    print()
    
    # Test d'instanciation
    try:
        print("🧪 Test d'instanciation d'ApiClient...")
        client = ApiClient()
        print(f"   ✅ ApiClient créé avec succès: {client}")
        print(f"   ✅ Interface users disponible: {hasattr(client, 'users')}")
        print(f"   ✅ Interface vms disponible: {hasattr(client, 'vms')}")
        print(f"   ✅ Interface auth disponible: {hasattr(client, 'auth')}")
        
        # Vérifier les types d'interfaces
        print(f"   ✅ Type users: {type(client.users)}")
        print(f"   ✅ Type vms: {type(client.vms)}")
        print(f"   ✅ Type auth: {type(client.auth)}")
        
    except Exception as e:
        print(f"   ❌ Erreur lors de l'instanciation: {e}")
        return False
    
    print("\n🎯 Résumé:")
    total_missing = len(missing_users) + len(missing_vms) + len(missing_auth) + len(missing_client)
    if total_missing == 0:
        print("   ✅ Toutes les méthodes de l'API sont correctement exposées dans ApiClient!")
        return True
    else:
        print(f"   ❌ {total_missing} méthodes manquantes détectées")
        return False

if __name__ == "__main__":
    success = test_api_exposure()
    sys.exit(0 if success else 1)
