#!/usr/bin/env python3
"""
Script de test pour le générateur de données Faker.
"""

import json
from utils.data_generator import DataGenerator, VMDataGenerator, UserDataGenerator


def test_vm_generator():
    """Test du générateur de VMs."""
    print("🧪 Test du générateur de VMs...")

    vm = VMDataGenerator.generate_vm(user_id=1, vm_id=1)

    print(f"✅ VM générée:")
    print(f"   • Nom: {vm['name']}")
    print(f"   • OS: {vm['operating_system']}")
    print(f"   • CPU: {vm['cpu_cores']} cœurs")
    print(f"   • RAM: {vm['ram_gb']} GB")
    print(f"   • Disque: {vm['disk_gb']} GB")
    print(f"   • Statut: {vm['status']}")
    print(f"   • Créé le: {vm['created_at']}")

    return vm


def test_user_generator():
    """Test du générateur d'utilisateurs."""
    print("\n🧪 Test du générateur d'utilisateurs...")

    user = UserDataGenerator.generate_user(user_id=1)

    print(f"✅ Utilisateur généré:")
    print(f"   • Nom: {user['name']}")
    print(f"   • Email: {user['email']}")
    print(f"   • Créé le: {user['created_at']}")
    print(f"   • VMs: {len(user['vms'])}")

    return user


def test_full_generator():
    """Test du générateur complet."""
    print("\n🧪 Test du générateur complet...")

    users_data = DataGenerator.generate_users_with_vms(
        user_count=5, vm_per_user_range=(0, 3)
    )

    print(f"✅ Dataset généré:")
    print(f"   • Utilisateurs: {len(users_data)}")

    total_vms = sum(len(user["vms"]) for user in users_data)
    print(f"   • VMs totales: {total_vms}")

    print("\n📋 Aperçu des données:")
    for i, user in enumerate(users_data, 1):
        print(f"   {i}. {user['name']} ({user['email']}) - {len(user['vms'])} VMs")
        if user["vms"]:
            for vm in user["vms"][:2]:  # Afficher max 2 VMs par utilisateur
                print(
                    f"      • {vm['name']} ({vm['operating_system']}) - {vm['status']}"
                )

    return users_data


def test_json_serialization():
    """Test de la sérialisation JSON."""
    print("\n🧪 Test de la sérialisation JSON...")

    users_data = DataGenerator.generate_users_with_vms(
        user_count=3, vm_per_user_range=(1, 2)
    )

    # Test de sérialisation
    json_str = json.dumps(users_data, indent=2, ensure_ascii=False, default=str)

    print(f"✅ Sérialisation JSON réussie")
    print(f"   • Taille: {len(json_str)} caractères")
    print(f"   • Structure valide: {len(json.loads(json_str))} utilisateurs")

    return json_str


if __name__ == "__main__":
    print("🎲 Test du générateur de données Faker")
    print("=" * 50)

    try:
        # Tests individuels
        test_vm_generator()
        test_user_generator()

        # Test complet
        users_data = test_full_generator()

        # Test JSON
        test_json_serialization()

        print("\n✅ Tous les tests sont passés avec succès !")
        print("🎉 Le générateur de données Faker est prêt à être utilisé.")

    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback

        traceback.print_exc()
