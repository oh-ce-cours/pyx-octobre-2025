#!/usr/bin/env python3
"""
Script de débogage pour tester la création d'utilisateurs
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent))

from utils.api import ApiClient
from utils.data_generator import UserDataGenerator
from utils.logging_config import get_logger

logger = get_logger(__name__)

def test_create_user():
    """Test de création d'un utilisateur avec logs détaillés"""
    print("🔍 Test de création d'utilisateur avec débogage")
    
    try:
        # Créer le client API
        api_client = ApiClient()
        print(f"✅ Client API créé: {api_client}")
        print(f"   Base URL: {api_client.base_url}")
        print(f"   Token: {api_client.token}")
        
        # Générer des données utilisateur
        user_data = UserDataGenerator.generate_user(1)
        print(f"✅ Données utilisateur générées: {user_data}")
        
        # Tenter de créer l'utilisateur
        print(f"🔄 Tentative de création d'utilisateur...")
        created_user = api_client.users.create_user(
            name=user_data["name"],
            email=user_data["email"],
            password="password123"
        )
        
        print(f"✅ Utilisateur créé: {created_user}")
        print(f"   Type: {type(created_user)}")
        print(f"   Est un dict: {isinstance(created_user, dict)}")
        if isinstance(created_user, dict):
            print(f"   Clés: {list(created_user.keys())}")
            print(f"   ID: {created_user.get('id')}")
        
        return created_user
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print(f"   Type d'erreur: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = test_create_user()
    print(f"\n📊 Résultat final: {result}")
