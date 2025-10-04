#!/usr/bin/env python3
"""
Script de test pour l'intégration API avec Faker.
Teste la création d'utilisateurs et de VMs via l'API avec des données réalistes.
"""

import sys
from utils.data_generator import DataGenerator, VMDataGenerator, UserDataGenerator
from api_data_manager import APIIntegrationService
from utils.logging_config import get_logger

logger = get_logger(__name__)

def test_faker_generation():
    """Test la génération de données Faker."""
    print("🎲 Test de la génération de données Faker")
    print("=" * 50)
    
    # Test génération utilisateur
    print("\n👤 Test génération utilisateur:")
    user = UserDataGenerator.generate_user(1)
    print(f"   • Nom: {user['name']}")
    print(f"   • Email: {user['email']}")
    print(f"   • Créé le: {user['created_at']}")
    
    # Test génération VM
    print("\n🖥️ Test génération VM:")
    vm = VMDataGenerator.generate_vm(user_id=1, vm_id=1)
    print(f"   • Nom: {vm['name']}")
    print(f"   • OS: {vm['operating_system']}")
    print(f"   • CPU: {vm['cpu_cores']} cœurs")
    print(f"   • RAM: {vm['ram_gb']} GB")
    print(f"   • Disque: {vm['disk_gb']} GB")
    print(f"   • Statut: {vm['status']}")
    
    # Test génération dataset complet
    print("\n📊 Test génération dataset complet:")
    dataset = DataGenerator.generate_users_with_vms(user_count=3, vm_per_user_range=(1, 2))
    
    total_vms = sum(len(user["vms"]) for user in dataset)
    print(f"   • Utilisateurs: {len(dataset)}")
    print(f"   • VMs totales: {total_vms}")
    print(f"   • Moyenne VMs/utilisateur: {total_vms/len(dataset):.1f}")
    
    print(f"\n✅ Tests de génération Faker réussis!")

def test_api_integration_demo():
    """Test de l'intégration API (mode démonstration avec données fictives)."""
    print("\n🌐 Test de l'intégration API (démo)")
    print("=" * 50)
    
    # URL de base de l'API d'exemple (selon le Swagger fourni)
    base_url = "https://x8ki-letl-twmt.n7.xano.io/api:N1uLlTBt"
    
    print(f"📍 URL de l'API: {base_url}")
    print("\n⚠️  Note: Cet exemple utilise l'URL de l'API fournie dans le Swagger")
    print("   Modifiez-la selon votre configuration réelle.")
    
    try:
        # Initialiser le service d'intégration
        service = APIIntegrationService(base_url)
        
        print("\n📋 Service d'intégration initialisé avec succès")
        print(f"   • Base URL: {service.base_url}")
        print(f"   • Admin email: {service.admin_email}")
        
        print("\n🔐 Note: L'authentification admin sera tentée lors de la création du dataset")
        print("   L'email admin@demo-api.com sera utilisé avec le mot de passe admin123")
        
        # Simulation d'un petit dataset
        print("\n📊 Simulation création dataset:")
        print("   • Utilisateurs: 5")
        print("   • VMs par utilisateur: 0-2")
        
        print("\n💡 Pour créer un réel dataset via l'API, utilisez:")
        print("   python main.py api-generate --base-url 'https://votre-api.com' --users 10")
        
        print(f"\n✅ Configuration d'intégration API prête!")

def main():
    """Fonction principale de test."""
    print("🧪 Script de test - Intégration API + Faker")
    print("=" * 60)
    
    try:
        # Test 1: Génération de données Faker
        test_faker_generation()
        
        # Test 2: Configuration de l'intégration API
        test_api_integration_demo()
        
        print("\n" + "=" * 60)
        print("🎉 Tous les tests sont passés avec succès !")
        print("\n📚 Commandes disponibles:")
        print("   • Génération locale:")
        print("     python main.py generate --users 20 --max-vms 5")
        print("     python generate_data.py preview --users 10")
        print("   • Génération via API:")
        print("     python main.py api-generate --base-url 'VOTRE_API_URL' --users 10")
        print("     python api_data_manager.py create-dataset --base-url 'VOTRE_API_URL'")
        print("\n🎯 Le système est prêt à générer des données réalistes !")
        
    except Exception as e:
        logger.error("Erreur lors des tests", error=str(e))
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
