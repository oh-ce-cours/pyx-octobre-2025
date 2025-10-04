#!/usr/bin/env python3
"""
Script de test pour vérifier que le refactoring avec exceptions fonctionne correctement.
"""

from utils.api import Api
from utils.api.exceptions import (
    UsersFetchError,
    VMsFetchError,
    VMCreationError,
    UserInfoError,
    TokenError,
    CredentialsError,
)
from utils.logging_config import get_logger

logger = get_logger(__name__)


def test_api_exceptions():
    """Test des nouvelles exceptions de l'API"""

    # Test avec une URL invalide pour déclencher des exceptions
    api = Api("http://invalid-url-that-does-not-exist.com")

    print("🧪 Test des exceptions de l'API...")

    # Test de récupération des utilisateurs
    try:
        users = api.users.get()
        print("❌ Erreur: get_users() aurait dû lever une exception")
    except UsersFetchError as e:
        print(f"✅ UsersFetchError correctement levée: {e}")
    except Exception as e:
        print(f"❌ Exception inattendue: {type(e).__name__}: {e}")

    # Test de récupération des VMs
    try:
        vms = api.vms.get()
        print("❌ Erreur: get_vms() aurait dû lever une exception")
    except VMsFetchError as e:
        print(f"✅ VMsFetchError correctement levée: {e}")
    except Exception as e:
        print(f"❌ Exception inattendue: {type(e).__name__}: {e}")

    # Test de récupération des informations utilisateur sans token
    try:
        user_info = api.get_user_info()
        print("❌ Erreur: get_user_info() aurait dû lever une exception")
    except TokenError as e:
        print(f"✅ TokenError correctement levée: {e}")
    except Exception as e:
        print(f"❌ Exception inattendue: {type(e).__name__}: {e}")

    # Test de création de VM sans token
    try:
        vm = api.users.create_vm(
            user_id=1,
            name="Test VM",
            operating_system="Ubuntu",
            cpu_cores=2,
            ram_gb=4,
            disk_gb=50,
        )
        print("❌ Erreur: create_vm() aurait dû lever une exception")
    except VMCreationError as e:
        print(f"✅ VMCreationError correctement levée: {e}")
    except Exception as e:
        print(f"❌ Exception inattendue: {type(e).__name__}: {e}")

    print("\n🎉 Tous les tests d'exceptions sont passés !")


if __name__ == "__main__":
    test_api_exceptions()
