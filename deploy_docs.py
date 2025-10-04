#!/usr/bin/env python3
"""
Script de déploiement complet pour GitHub Pages.
Remplace deploy_docs.sh avec une meilleure compatibilité cross-platform.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


# Configuration
BASE_URL = "https://oh-ce-cours.github.io/pyx-octobre-2025/docs-deploy"
PROJECT_ROOT = Path(__file__).parent
DEMO_API_DIR = PROJECT_ROOT / "tape_en_cours" / "demo_api"
DOCS_DEPLOY_DIR = PROJECT_ROOT / "docs-deploy"


def run_command(command: str, description: str, cwd: Path = None) -> bool:
    """
    Exécute une commande et affiche le résultat.
    
    Args:
        command: Commande à exécuter
        description: Description de la commande
        cwd: Répertoire de travail (optionnel)
        
    Returns:
        True si la commande a réussi, False sinon
    """
    print(f"\n🔄 {description}...")
    print(f"📝 Commande: {command}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        print(f"✅ {description} - Succès")
        if result.stdout:
            print(f"📤 Sortie: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erreur")
        if e.stdout:
            print(f"📤 Sortie: {e.stdout}")
        if e.stderr:
            print(f"📤 Erreur: {e.stderr}")
        return False


def fix_static_paths(file_path: Path) -> bool:
    """
    Corrige les chemins _static vers static dans un fichier.
    
    Args:
        file_path: Chemin vers le fichier à corriger
        
    Returns:
        True si des modifications ont été apportées, False sinon
    """
    try:
        # Lire le fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Déterminer l'URL de base selon la structure
        if "/sphinx/" in str(file_path):
            base_url = f"{BASE_URL}/sphinx"
        elif "/pdoc3/" in str(file_path):
            base_url = f"{BASE_URL}/pdoc3"
        else:
            base_url = BASE_URL
        
        # Patterns à remplacer
        patterns = [
            # Chemins directs _static/
            (r'href="_static/', f'href="{base_url}/static/'),
            (r'src="_static/', f'src="{base_url}/static/'),
            (r'url\("_static/', f'url("{base_url}/static/'),
            (r"url\('_static/", f"url('{base_url}/static/"),
            
            # Chemins relatifs ../_static/
            (r'href="../_static/', f'href="{base_url}/static/'),
            (r'src="../_static/', f'src="{base_url}/static/'),
            (r'url\("../_static/', f'url("{base_url}/static/'),
            (r"url\('../_static/", f"url('{base_url}/static/"),
        ]
        
        # Appliquer les remplacements
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        # Écrire le fichier modifié seulement s'il y a eu des changements
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Corrigé: {file_path}")
            return True
        else:
            print(f"⏭️  Aucun changement: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du traitement de {file_path}: {e}")
        return False


def create_nojekyll_file():
    """Crée le fichier .nojekyll pour désactiver Jekyll sur GitHub Pages."""
    nojekyll_path = DOCS_DEPLOY_DIR / ".nojekyll"
    nojekyll_path.touch()
    print("✅ Fichier .nojekyll créé pour désactiver Jekyll sur GitHub Pages")


def create_robots_txt():
    """Crée le fichier robots.txt pour éviter l'indexation des dossiers techniques."""
    robots_path = DOCS_DEPLOY_DIR / "robots.txt"
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write("User-agent: *\n")
        f.write("Disallow: /_static/\n")
        f.write("Disallow: /_sources/\n")
    print("✅ Fichier robots.txt créé")


def copy_static_folder():
    """Crée une copie du dossier _static en static pour GitHub Pages."""
    sphinx_static_src = DOCS_DEPLOY_DIR / "sphinx" / "_static"
    sphinx_static_dst = DOCS_DEPLOY_DIR / "sphinx" / "static"
    
    if sphinx_static_src.exists():
        if sphinx_static_dst.exists():
            shutil.rmtree(sphinx_static_dst)
        shutil.copytree(sphinx_static_src, sphinx_static_dst)
        print("✅ Dossier static/ créé à partir de _static/")
    else:
        print("⚠️  Dossier _static non trouvé")


def main():
    """Fonction principale."""
    print("🚀 Script de déploiement Python pour GitHub Pages")
    print("=" * 50)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not DEMO_API_DIR.exists():
        print("❌ Erreur: Répertoire demo_api non trouvé")
        sys.exit(1)
    
    success_count = 0
    total_commands = 0
    
    # 1. Générer les modules avec le script d'auto-découverte
    total_commands += 1
    if run_command(
        "python docs/sphinx/source/generate_modules.py",
        "Auto-découverte des modules Sphinx",
        cwd=DEMO_API_DIR
    ):
        success_count += 1
    
    # 2. Générer la documentation Sphinx
    total_commands += 1
    if run_command(
        "sphinx-build -b html source build",
        "Génération de la documentation Sphinx",
        cwd=DEMO_API_DIR / "docs" / "sphinx"
    ):
        success_count += 1
    
    # 3. Générer la documentation pdoc3 avec index complet
    total_commands += 1
    if run_command(
        "pdoc --html -o docs/pdoc3 . --force",
        "Génération de la documentation pdoc3 complète",
        cwd=DEMO_API_DIR
    ):
        success_count += 1
    
    # 4. Créer le dossier docs-deploy
    print("\n📁 Préparation des fichiers pour GitHub Pages...")
    if DOCS_DEPLOY_DIR.exists():
        shutil.rmtree(DOCS_DEPLOY_DIR)
    DOCS_DEPLOY_DIR.mkdir()
    
    # 5. Copier la documentation Sphinx
    sphinx_build_dir = DEMO_API_DIR / "docs" / "sphinx" / "build"
    if sphinx_build_dir.exists():
        shutil.copytree(sphinx_build_dir, DOCS_DEPLOY_DIR / "sphinx")
        print("✅ Documentation Sphinx copiée")
    
    # 6. Copier la documentation pdoc3
    pdoc3_dir = DEMO_API_DIR / "docs" / "pdoc3"
    if pdoc3_dir.exists():
        shutil.copytree(pdoc3_dir, DOCS_DEPLOY_DIR / "pdoc3")
        print("✅ Documentation pdoc3 copiée")
    
    # 7. Créer le fichier index principal
    index_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demo API - Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { text-align: center; }
        .doc-link { display: inline-block; margin: 20px; padding: 20px; border: 2px solid #007acc; border-radius: 8px; text-decoration: none; color: #007acc; }
        .doc-link:hover { background-color: #007acc; color: white; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Demo API - Documentation</h1>
        <p>Choisissez votre format de documentation préféré :</p>
        
        <a href="sphinx/index.html" class="doc-link">
            <h3>📚 Sphinx (Complet)</h3>
            <p>Documentation détaillée avec navigation avancée</p>
        </a>
        
        <a href="pdoc3/index.html" class="doc-link">
            <h3>⚡ pdoc3 (Moderne)</h3>
            <p>Documentation moderne avec interface épurée</p>
        </a>
    </div>
</body>
</html>"""
    
    with open(DOCS_DEPLOY_DIR / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_content)
    print("✅ Page d'accueil créée")
    
    # 8. Créer les fichiers de configuration GitHub Pages
    create_nojekyll_file()
    create_robots_txt()
    
    # 9. Créer une copie static/ pour GitHub Pages
    copy_static_folder()
    
    # 10. Corriger les chemins dans tous les fichiers
    print("\n🔧 Correction des chemins CSS pour GitHub Pages...")
    files_to_fix = []
    
    # Trouver tous les fichiers HTML, CSS et JS
    for pattern in ["*.html", "*.css", "*.js"]:
        files_to_fix.extend(DOCS_DEPLOY_DIR.rglob(pattern))
    
    fixed_count = 0
    for file_path in files_to_fix:
        if fix_static_paths(file_path):
            fixed_count += 1
    
    print(f"✅ {fixed_count} fichiers corrigés")
    
    # Résumé
    print("\n" + "=" * 50)
    print(f"📊 Résumé: {success_count}/{total_commands} commandes réussies")
    
    if success_count == total_commands:
        print("🎉 Toute la documentation a été générée avec succès!")
        print("\n📖 Documentation disponible:")
        print(f"   • Sphinx (complexe): {DOCS_DEPLOY_DIR}/sphinx/index.html")
        print(f"   • pdoc3 (moderne): {DOCS_DEPLOY_DIR}/pdoc3/index.html")
        print("\n📋 Prochaines étapes :")
        print("   1. git add docs-deploy/")
        print("   2. git commit -m 'Deploy documentation to GitHub Pages'")
        print("   3. git push origin main")
        print(f"\n🌐 Après push, GitHub Pages sera disponible sur :")
        print(f"   {BASE_URL}/")
    else:
        print("⚠️  Certaines commandes ont échoué. Vérifiez les erreurs ci-dessus.")
        sys.exit(1)


if __name__ == "__main__":
    main()
