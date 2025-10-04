#!/usr/bin/env python3
"""
Script de génération de documentation complète.

Ce script génère automatiquement la documentation avec Sphinx et pydoc.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """
    Exécute une commande et affiche le résultat.
    
    Args:
        command: Commande à exécuter
        description: Description de la commande
    
    Returns:
        True si la commande a réussi, False sinon
    """
    print(f"\n🔄 {description}...")
    print(f"📝 Commande: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Succès")
        if result.stdout:
            print(f"📤 Sortie: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erreur")
        print(f"📤 Sortie: {e.stdout}")
        print(f"📤 Erreur: {e.stderr}")
        return False


def main():
    """Fonction principale."""
    project_root = Path(__file__).parent.parent
    
    print("📚 Génération de la documentation Demo API")
    print("=" * 50)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not (project_root / "main.py").exists():
        print("❌ Erreur: Ce script doit être exécuté depuis la racine du projet")
        sys.exit(1)
    
    success_count = 0
    total_commands = 0
    
    # 1. Générer les modules avec le script d'auto-découverte
    total_commands += 1
    if run_command(
        f"cd {project_root} && python docs/sphinx/source/generate_modules.py",
        "Auto-découverte des modules Sphinx"
    ):
        success_count += 1
    
    # 2. Générer la documentation Sphinx
    total_commands += 1
    if run_command(
        f"cd {project_root}/docs/sphinx && sphinx-build -b html source build",
        "Génération de la documentation Sphinx"
    ):
        success_count += 1
    
    # 3. Générer la documentation pydoc
    total_commands += 1
    if run_command(
        f"cd {project_root} && python docs/pydoc/generate_pydoc.py",
        "Génération de la documentation pydoc"
    ):
        success_count += 1
    
    # Résumé
    print("\n" + "=" * 50)
    print(f"📊 Résumé: {success_count}/{total_commands} commandes réussies")
    
    if success_count == total_commands:
        print("🎉 Toute la documentation a été générée avec succès!")
        print("\n📖 Documentation disponible:")
        print(f"   • Sphinx: {project_root}/docs/sphinx/build/index.html")
        print(f"   • pydoc: {project_root}/docs/pydoc/html/index.html")
    else:
        print("⚠️  Certaines commandes ont échoué. Vérifiez les erreurs ci-dessus.")
        sys.exit(1)


if __name__ == "__main__":
    main()
