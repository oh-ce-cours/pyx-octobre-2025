#!/usr/bin/env python3
"""
Script de déploiement de documentation sur GitHub Pages.

Ce script prépare la documentation pour GitHub Pages et configure
le dépôt pour servir les fichiers statiques.
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
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
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

    print("🚀 Déploiement documentation Demo API")
    print("=" * 50)

    # Vérifier que nous sommes dans le bon répertoire
    if not (project_root / "main.py").exists():
        print("❌ Erreur: Ce script doit être exécuté depuis la racine du projet")
        sys.exit(1)

    success_count = 0
    total_commands = 0

    # 1. Générer la documentation complète
    total_commands += 1
    if run_command(
        f"cd {project_root} && python scripts/generate_docs.py",
        "Génération de la documentation complète",
    ):
        success_count += 1

    # 2. Préparer les fichiers pour GitHub Pages
    total_commands += 1
    if run_command(
        f"cd {project_root} && mkdir -p docs-deploy && cp -r docs/sphinx/build/* docs-deploy/",
        "Préparation des fichiers pour déploiement",
    ):
        success_count += 1

    # 3. Ajouter .nojekyll pour GitHub Pages
    total_commands += 1
    if run_command(
        f"cd {project_root} && touch docs-deploy/.nojekyll",
        "Ajout du fichier .nojekyll pour GitHub Pages",
    ):
        success_count += 1

    # Résumé
    print("\n" + "=" * 50)
    print(f"📊 Résumé: {success_count}/{total_commands} commandes réussies")

    if success_count == total_commands:
        print("🎉 Documentation prête pour GitHub Pages!")
        print("\n📖 Prochaines étapes:")
        print(f"   1. Commitez le dossier docs-deploy/")
        print(f"   2. Poussez vers GitHub")
        print(f"   3. Activez GitHub Pages dans les settings du repo")
        print(f"   4. Ouvrez : https://votrenom.github.io/votre-repo/")

        print(f"\n💡 Alternative : Utilisez l'action GitHub CI/CD")
        print(f"   - Un commit sur main déploiera automatiquement")
        print(f"   - Cf. .github/workflows/docs.yml")
    else:
        print("⚠️  Certaines commandes ont échoué. Vérifiez les erreurs ci-dessus.")


if __name__ == "__main__":
    main()
