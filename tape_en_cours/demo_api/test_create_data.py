#!/usr/bin/env python3
"""
Script de test pour valider le fonctionnement du créateur de données via API.
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent))

from utils.data_generator import UserDataGenerator, VMDataGenerator
from utils.logging_config import get_logger

logger = get_logger(__name__)


def test_data_generators():
    """Test des générateurs de données Faker"""
    print("🧪 Test des générateurs de données Faker...")
    
    # Test génération utilisateur
    print("\n👤 Test génération utilisateur:")
    user = UserDataGenerator.generate_user(1)
    print(f"   Nom: {user['name']}")
    print(f"   Email: {user['email']}")
    print(f"   Créé le: {user['created_at']}")
    
    # Test génération VM
    print("\n🖥️ Test génération VM:")
    vm = VMDataGenerator.generate_vm(user_id=1, vm_id=1)
    print(f"   Nom: {vm['name']}")
    print(f"   OS: {vm['operating_system']}")
    print(f"   CPU: {vm['cpu_cores']} cœurs")
    print(f"   RAM: {vm['ram_gb']} GB")
    print(f"   Disque: {vm['disk_gb']} GB")
    print(f"   Statut: {vm['status']}")
    
    print("\n✅ Tests des générateurs réussis !")


def test_api_imports():
    """Test des imports de l'API"""
    print("\n🔌 Test des imports API...")
    
    try:
        from utils.api import ApiClient, create_authenticated_client
        print("   ✅ Import ApiClient réussi")
        print("   ✅ Import create_authenticated_client réussi")
        
        # Test création client sans authentification
        client = ApiClient()
        print(f"   ✅ Client créé avec URL: {client.base_url}")
        
    except ImportError as e:
        print(f"   ❌ Erreur d'import: {e}")
        return False
    
    print("✅ Tests des imports API réussis !")
    return True


def main():
    """Point d'entrée principal des tests"""
    print("🚀 Tests du créateur de données via API")
    print("=" * 50)
    
    try:
        # Test 1: Générateurs de données
        test_data_generators()
        
        # Test 2: Imports API
        if not test_api_imports():
            print("\n❌ Tests échoués - problèmes d'imports")
            return 1
        
        print("\n🎉 Tous les tests sont passés avec succès !")
        print("\n💡 Vous pouvez maintenant utiliser le script create_data_via_api.py")
        print("   Exemples:")
        print("   python create_data_via_api.py users --count 5")
        print("   python create_data_via_api.py vms --count 10")
        print("   python create_data_via_api.py status")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        logger.error("Erreur lors des tests", error=str(e))
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
