#!/usr/bin/env python3
"""
Démonstration de l'utilisation du token sauvegardé
"""

import os
from utils.password_utils import get_token_from_env, save_token_to_env


def demo_token_usage():
    """Démontre l'utilisation du token dans la console"""

    print("🔑 Démonstration de la gestion des tokens")
    print("=" * 50)

    # Vérifier s'il y a un token sauvegardé
    token = get_token_from_env()

    if token:
        print(f"✅ Token trouvé dans la session: {token[:20]}...")
        print(f"   Longueur: {len(token)} caractères")
        print(f"   Variable d'environnement: DEMO_API_TOKEN")
    else:
        print("❌ Aucun token trouvé dans la session")
        print(
            "💡 Utilisez 'python main.py signup' pour créer un utilisateur et sauvegarder un token"
        )

    print()
    print("📋 Commandes disponibles:")
    print("   1. python main.py signup --name 'Mon Nom' --email 'mon@email.com'")
    print("      → Crée un utilisateur et sauvegarde le token")
    print()
    print("   2. python main.py create --name 'Ma VM' --use-token")
    print("      → Crée une VM en utilisant le token sauvegardé")
    print()
    print(
        "   3. python main.py create --name 'Ma VM' --email 'mon@email.com' --password 'motdepasse'"
    )
    print("      → Crée une VM avec authentification email/mot de passe")
    print()

    # Afficher les variables d'environnement liées aux tokens
    print("🔍 Variables d'environnement actuelles:")
    token_vars = ["DEMO_API_TOKEN", "DEMO_API_EMAIL", "DEMO_API_PASSWORD"]
    for var in token_vars:
        value = os.environ.get(var)
        if value:
            if "TOKEN" in var:
                print(f"   {var}: {value[:20]}... (longueur: {len(value)})")
            else:
                print(f"   {var}: {value}")
        else:
            print(f"   {var}: Non définie")


if __name__ == "__main__":
    demo_token_usage()
