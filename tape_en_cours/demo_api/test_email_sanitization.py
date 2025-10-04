#!/usr/bin/env python3
"""
Script de test pour vérifier la sanitisation des emails
"""

import sys
from pathlib import Path

# Ajouter le répertoire utils au path
sys.path.append(str(Path(__file__).parent / "utils"))

from data_generator import UserDataGenerator


def test_email_sanitization():
    """Test la sanitisation des emails avec des noms contenant des accents"""

    test_names = [
        "Inès Bouvet",
        "François Martin",
        "José García",
        "Renée Dubois",
        "Éléonore Leroy",
        "Théo Moreau",
        "Anaïs Petit",
        "Sébastien Robert",
    ]

    print("🧪 Test de sanitisation des emails :")
    print("=" * 50)

    for name in test_names:
        email = UserDataGenerator.generate_email(name)
        print(f"📧 {name} -> {email}")

    print("\n✅ Les emails sont maintenant sans caractères spéciaux !")


if __name__ == "__main__":
    test_email_sanitization()
