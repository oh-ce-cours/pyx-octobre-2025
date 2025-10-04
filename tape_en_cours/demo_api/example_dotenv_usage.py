#!/usr/bin/env python3
"""
Exemple d'utilisation de python-dotenv dans demo_api
"""

import sys
import os

# Ajouter le répertoire courant au PYTHONPATH pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.password_utils import (
    load_env_files,
    save_token_to_env_file,
    load_token_from_env_file,
    get_credentials_from_env,
)

def demo_env_loading():
    """Démontre le chargement automatique des fichiers .env"""
    print("\n=== Démontration du chargement de fichiers .env ===")
    
    print("1. Chargement automatique des fichiers .env")
    print("   Hierarchie: .env.defaults → .env.local → .env")
    
    loaded_count = load_env_files()
    print(f"   ✅ {loaded_count} fichier(s) .env chargé(s)")
    
    print("\n2. Variables d'environnement chargées:")
    env_vars = [
        "DEMO_API_EMAIL",
        "DEMO_API_PASSWORD", 
        "DEMO_API_TOKEN",
        "DEMO_API_DEBUG",
        "DEMO_API_LOG_LEVEL"
    ]
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            masked_value = "*" * len(value) if "PASSWORD" in var or "TOKEN" in var else value
            print(f"   {var} = {masked_value}")
        else:
            print(f"   {var} = (non défini)")

def demo_token_file_management():
    """Démontre la gestion des tokens avec python-dotenv"""
    print("\n=== Gestion des tokens avec fichiers .env ==="]
    
    # Token fictif pour l'exemple
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example.python_dotenv_token"
    
    print("1. Sauvegarde d'un token avec python-dotenv")
    success = save_token_to_env_file(fake_token, ".env.example", "DEMO_API_TOKEN")
    print(f"   ✅ Token sauvegardé: {success}")
    
    print("2. Chargement d'un token avec python-dotenv")
    loaded_token = load_token_from_env_file(".env.example", "DEMO_API_TOKEN")
    print(f"   ✅ Token chargé: {'*' * len(loaded_token) if loaded_token else 'None'}")

def demo_credentials_from_env():
    """Démontre la récupération d'identifiants depuis les fichiers .env"""
    print("\n=== Récupération d'identifiants depuis .env ===")
    
    credentials = get_credentials_from_env()
    
    if credentials:
        email, password = credentials
        print(f"   ✅ Identifiants trouvés:")
        print(f"      Email: {email}")
        print(f"      Password: {'*' * len(password)}")
    else:
        print("   ℹ️  Identifiants incomplets dans les fichiers .env")

def demo_file_hierarchy():
    """Démontre la hiérarchie des fichiers .env"""
    print("\n=== Hiérarchie des fichiers .env ===")
    
    env_files_info = [
        (".env.defaults", "Valeurs par défaut (versionné)"),
        (".env.local", "Configuration locale (équipe)"),
        (".env", "Configuration générale (partagée)")
    ]
    
    for env_file, description in env_files_info:
        exists = os.path.exists(env_file)
        status = "✅ Existe" if exists else "❌ Absent"
        print(f"   {env_file:<15} {status:<10} {description}")
        
        if exists:
            # Montrer quelques lignes du fichier (max 3)
            try:
                with open(env_file, 'r') as f:
                    lines = f.readlines()
                    print(f"      Aperçu ({len(lines)} lignes):")
                    for line in lines[:3]:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Masquer les valeurs sensibles
                            if '=' in line:
                                key, value = line.split('=', 1)
                                if 'PASSWORD' in key or 'TOKEN' in key:
                                    line = f"{key}=***"
                            print(f"        {line}")
            except Exception as e:
                print(f"        Erreur lecture: {e}")

if __name__ == "__main__":
    print("🔧 Démontration de python-dotenv dans demo_api")
    
    demo_env_loading()
    demo_token_file_management()
    demo_credentials_from_env()
    demo_file_hierarchy()
    
    print("\n✅ Démonstration terminée!")
    print("\n💡 Workflow recommandé:")
    print("   1. cp env.example .env")
    print("   2. Éditer .env avec vos vraies valeurs")
    print("   3. (optionnel) Créer .env.local pour des valeurs sensibles")
    print("   4. python main.py  # Chargement automatique des .env")
