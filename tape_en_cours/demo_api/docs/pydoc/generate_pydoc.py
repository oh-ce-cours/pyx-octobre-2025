#!/usr/bin/env python3
"""
Script de génération de documentation avec pydoc.

Ce script utilise pydoc pour générer automatiquement la documentation
HTML de tous les modules Python du projet.
"""

import os
import sys
import pydoc
import subprocess
from pathlib import Path
from typing import List, Dict


def find_python_modules(root_dir: Path, exclude_dirs: set = None) -> List[Dict]:
    """
    Trouve tous les modules Python dans le répertoire donné.

    Args:
        root_dir: Répertoire racine à explorer
        exclude_dirs: Dossiers à exclure

    Returns:
        Liste des modules Python trouvés
    """
    if exclude_dirs is None:
        exclude_dirs = {
            "__pycache__",
            ".git",
            ".pytest_cache",
            "docs",
            "outputs",
            "templates",
        }

    modules = []

    for py_file in root_dir.rglob("*.py"):
        # Ignorer les fichiers dans les dossiers exclus
        if any(part in exclude_dirs for part in py_file.parts):
            continue

        # Ignorer les fichiers __init__.py vides ou les fichiers de test
        if py_file.name.startswith("test_") or py_file.name == "__init__.py":
            continue

        # Convertir le chemin en nom de module
        relative_path = py_file.relative_to(root_dir)
        module_name = str(relative_path.with_suffix("")).replace("/", ".")

        modules.append(
            {"name": module_name, "path": py_file, "relative_path": relative_path}
        )

    return sorted(modules, key=lambda x: x["name"])


def generate_pydoc_html(module_name: str, output_dir: Path, project_root: Path) -> None:
    """
    Génère la documentation HTML pour un module avec pydoc.

    Args:
        module_name: Nom du module
        output_dir: Répertoire de sortie
        project_root: Racine du projet
    """
    try:
        # Ajouter le répertoire du projet au PYTHONPATH
        import sys

        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        # Créer le répertoire de destination
        html_file = output_dir / f"{module_name}.html"
        html_file.parent.mkdir(parents=True, exist_ok=True)

        # Générer la documentation HTML avec pydoc
        try:
            # Essayer d'importer le module pour vérifier qu'il existe
            import importlib
            module = importlib.import_module(module_name)
            
            # Générer la documentation HTML avec pydoc
            html_doc = pydoc.HTMLDoc()
            html_content = html_doc.document(module)
        except Exception as import_error:
            # Si l'import échoue, générer une documentation basique
            html_content = f"""
            <h1>Module: {module_name}</h1>
            <p><strong>Erreur d'import:</strong> {import_error}</p>
            <p>Ce module n'a pas pu être importé correctement.</p>
            """
        
        # Ajouter un en-tête HTML complet
        full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{module_name} - Documentation pydoc</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        h1 {{ color: #333; border-bottom: 2px solid #eee; }}
        h2 {{ color: #666; margin-top: 30px; }}
        h3 {{ color: #888; }}
        .back-link {{ margin-bottom: 20px; }}
        .back-link a {{ color: #0066cc; text-decoration: none; }}
        .back-link a:hover {{ text-decoration: underline; }}
        pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        code {{ background-color: #f5f5f5; padding: 2px 4px; border-radius: 3px; }}
        .function {{ margin: 15px 0; }}
        .class {{ margin: 20px 0; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="back-link">
        <a href="index.html">← Retour à l'index</a>
    </div>
    {html_content}
</body>
</html>"""

        # Écrire le fichier HTML complet
        html_file.write_text(full_html, encoding="utf-8")

        print(f"✓ Généré: {html_file}")

    except Exception as e:
        print(f"✗ Erreur pour {module_name}: {e}")


def generate_index_html(modules: List[Dict], output_dir: Path) -> None:
    """
    Génère un fichier index.html avec tous les modules.

    Args:
        modules: Liste des modules trouvés
        output_dir: Répertoire de sortie
    """
    html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demo API - Documentation pydoc</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        .module-list { list-style-type: none; padding: 0; }
        .module-list li { margin: 10px 0; }
        .module-list a { text-decoration: none; color: #0066cc; }
        .module-list a:hover { text-decoration: underline; }
        .module-category { margin-top: 30px; }
        .module-category h2 { color: #666; border-bottom: 2px solid #eee; }
    </style>
</head>
<body>
    <h1>Demo API - Documentation pydoc</h1>
    <p>Documentation automatique générée avec pydoc pour tous les modules Python du projet.</p>
    
    <div class="module-category">
        <h2>Modules principaux</h2>
        <ul class="module-list">
"""

    # Grouper les modules par catégorie
    main_modules = [
        m
        for m in modules
        if not m["name"].startswith(("utils.", "reports.", "scripts."))
    ]
    utils_modules = [m for m in modules if m["name"].startswith("utils.")]
    reports_modules = [m for m in modules if m["name"].startswith("reports.")]
    scripts_modules = [m for m in modules if m["name"].startswith("scripts.")]

    # Ajouter les modules principaux
    for module in main_modules:
        html_content += f'            <li><a href="{module["name"]}.html">{module["name"]}</a></li>\n'

    html_content += """        </ul>
    </div>
    
    <div class="module-category">
        <h2>Modules utilitaires</h2>
        <ul class="module-list">
"""

    # Ajouter les modules utilitaires
    for module in utils_modules:
        html_content += f'            <li><a href="{module["name"]}.html">{module["name"]}</a></li>\n'

    html_content += """        </ul>
    </div>
    
    <div class="module-category">
        <h2>Modules de rapports</h2>
        <ul class="module-list">
"""

    # Ajouter les modules de rapports
    for module in reports_modules:
        html_content += f'            <li><a href="{module["name"]}.html">{module["name"]}</a></li>\n'

    html_content += """        </ul>
    </div>
    
    <div class="module-category">
        <h2>Scripts</h2>
        <ul class="module-list">
"""

    # Ajouter les scripts
    for module in scripts_modules:
        html_content += f'            <li><a href="{module["name"]}.html">{module["name"]}</a></li>\n'

    html_content += """        </ul>
    </div>
    
    <hr>
    <p><em>Documentation générée automatiquement avec pydoc</em></p>
</body>
</html>"""

    # Écrire le fichier index
    index_path = output_dir / "index.html"
    index_path.write_text(html_content, encoding="utf-8")
    print(f"✓ Généré: {index_path}")


def main():
    """Fonction principale."""
    # Définir les chemins
    project_root = Path(__file__).parent.parent.parent
    output_dir = Path(__file__).parent / "html"

    print(f"🔍 Exploration du projet: {project_root}")
    print(f"📁 Répertoire de sortie: {output_dir}")

    # Créer le répertoire de sortie
    output_dir.mkdir(parents=True, exist_ok=True)

    # Trouver tous les modules Python
    modules = find_python_modules(project_root)

    print(f"📦 {len(modules)} modules trouvés:")
    for module in modules:
        print(f"  - {module['name']}")

    # Générer la documentation HTML pour chaque module
    print("\n📝 Génération de la documentation HTML...")
    for module in modules:
        generate_pydoc_html(module["name"], output_dir, project_root)

    # Générer le fichier index
    print("\n📋 Génération du fichier index...")
    generate_index_html(modules, output_dir)

    print(f"\n✅ Documentation pydoc générée avec succès!")
    print(f"📖 {len(modules)} modules documentés dans {output_dir}")
    print(f"🌐 Ouvrez {output_dir / 'index.html'} dans votre navigateur")


if __name__ == "__main__":
    main()
