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

        # Ajouter un en-tête HTML complet avec CSS complet pour pydoc
        full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{module_name} - Documentation pydoc</title>
    <style>
        /* Reset et styles de base */
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif; 
            margin: 20px; 
            line-height: 1.6; 
            background-color: #fff;
            color: #333;
        }}
        
        /* Styles pour la navigation */
        .back-link {{ 
            margin-bottom: 20px; 
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
        .back-link a {{ 
            color: #0066cc; 
            text-decoration: none; 
            font-weight: 500;
        }}
        .back-link a:hover {{ 
            text-decoration: underline; 
        }}
        
        /* Styles pour les titres pydoc */
        h1, h2, h3, h4, h5, h6 {{
            color: #333;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        
        /* Styles pour les tableaux pydoc */
        table.heading {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            background-color: #f8f9fa;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .heading-text {{
            padding: 15px 20px;
        }}
        
        .title {{
            font-size: 1.5em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .extra {{
            text-align: right;
            vertical-align: top;
            padding: 15px 20px;
        }}
        
        .extra a {{
            color: #6c757d;
            text-decoration: none;
            font-size: 0.9em;
        }}
        
        .extra a:hover {{
            color: #0066cc;
        }}
        
        /* Sections pydoc */
        table.section {{
            width: 100%;
            margin: 20px 0;
            border-collapse: collapse;
            background-color: white;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            overflow: hidden;
        }}
        
        .section-title {{
            background-color: #e9ecef;
            padding: 12px 15px;
            font-weight: bold;
            color: #495057;
            border-bottom: 1px solid #dee2e6;
        }}
        
        .bigsection {{
            font-size: 1.1em;
        }}
        
        /* Styles pour les éléments de contenu */
        .code {{
            background-color: transparent;
            font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
            white-space: pre-wrap;
            color: #444;
            font-size: 0.95em;
        }}
        
        pre {{
            background-color: #f8f9fa; 
            padding: 15px; 
            border-radius: 8px; 
            overflow-x: auto;
            border: 1px solid #e9ecef;
            font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
        }}
        
        code {{
            background-color: #f1f3f4; 
            padding: 3px 6px; 
            border-radius: 4px; 
            font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
            font-size: 0.9em;
            color: #d73a49;
        }}
        
        /* Styles pour les fonctions et classes */
        .function {{ 
            margin: 20px 0; 
            padding: 15px;
            background-color: #f8f9fa;
            border-left: 4px solid #0066cc;
            border-radius: 0 5px 5px 0;
        }}
        
        .class {{ 
            margin: 25px 0; 
            border: 1px solid #dee2e6; 
            padding: 20px; 
            border-radius: 8px;
            background-color: #fff;
        }}
        
        /* Styles pour les liens */
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        /* Styles pour les listes */
        ul, ol {{
            margin-left: 20px;
        }}
        
        li {{
            margin-bottom: 5px;
        }}
        
        /* Styles pour les descriptions */
        p {{
            margin-bottom: 15px;
            color: #555;
        }}
        
        /* Styles spécifiques pour les decorators pydoc */
        .decor {{
            vertical-align: top;
            width: 20px;
        }}
        
        .pkg-content-decor, .index-decor {{
            background-color: #f8f9fa;
            border-right: 1px solid #dee2e6;
            width: 30px;
        }}
        
        .multicolumn {{
            width: 25%;
            vertical-align: top;
        }}
        
        .multicolumn a {{
            color: #0066cc;
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            body {{
                margin: 10px;
            }}
            
            table.heading {{
                font-size: 0.9em;
            }}
            
            .extra {{
                text-align: left;
                padding-top: 10px;
            }}
        }}
        
        /* Amélioration de lisibilité */
        .singlecolumn {{
            padding: 15px;
        }}
        
        dt.heading-text {{
            font-weight: bold;
            color: #2c3e50;
            margin-top: 15px;
        }}
        
        dd {{
            margin-left: 0;
            margin-bottom: 20px;
            padding-left: 20px;
        }}
    </style>
</head>
<body>
    <div class="back-link">
        <a href="index.html">← Retour à l'index des modules</a>
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
