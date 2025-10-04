#!/usr/bin/env python3
"""
Script d'auto-découverte des modules Python pour Sphinx.

Ce script parcourt automatiquement le projet et génère les fichiers .rst
pour tous les modules Python trouvés.
"""

import os
import sys
from pathlib import Path


def find_python_modules(root_dir: Path, exclude_dirs: set = None) -> list:
    """
    Trouve tous les modules Python dans le répertoire donné.

    Args:
        root_dir: Répertoire racine à explorer
        exclude_dirs: Dossiers à exclure (ex: __pycache__, .git, etc.)

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


def generate_module_rst(module_info: dict, output_dir: Path) -> None:
    """
    Génère un fichier .rst pour un module donné.

    Args:
        module_info: Informations sur le module
        output_dir: Répertoire de sortie pour les fichiers .rst
    """
    module_name = module_info["name"]
    relative_path = module_info["relative_path"]

    # Créer le répertoire de destination
    rst_path = output_dir / relative_path.with_suffix(".rst")
    rst_path.parent.mkdir(parents=True, exist_ok=True)

    # Générer le contenu du fichier .rst
    content = f"""Module {module_name}
{"=" * (len(module_name) + 7)}

.. automodule:: {module_name}
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__
"""

    # Écrire le fichier
    rst_path.write_text(content, encoding="utf-8")
    print(f"✓ Généré: {rst_path}")


def generate_index_rst(modules: list, output_dir: Path) -> None:
    """
    Génère un fichier index.rst avec tous les modules.

    Args:
        modules: Liste des modules trouvés
        output_dir: Répertoire de sortie
    """
    # Grouper les modules par répertoire
    modules_by_dir = {}
    for module in modules:
        dir_path = module["relative_path"].parent
        if dir_path not in modules_by_dir:
            modules_by_dir[dir_path] = []
        modules_by_dir[dir_path].append(module)

    # Générer le contenu
    content = ["Modules API", "=" * 10, ""]

    for dir_path in sorted(modules_by_dir.keys()):
        if dir_path == Path("."):
            section_title = "Modules principaux"
        else:
            section_title = f"Modules {dir_path}"

        content.extend([section_title, "-" * len(section_title), ""])

        for module in modules_by_dir[dir_path]:
            module_name = module["name"]
            rst_file = module["relative_path"].with_suffix(".rst")
            content.append(f".. toctree::")
            content.append(f"   :maxdepth: 4")
            content.append(f"")
            content.append(f"   {rst_file}")
            content.append("")

    # Écrire le fichier index
    index_path = output_dir / "index.rst"
    index_path.write_text("\n".join(content), encoding="utf-8")
    print(f"✓ Généré: {index_path}")


def main():
    """Fonction principale."""
    # Définir les chemins
    project_root = Path(__file__).parent.parent.parent.parent
    output_dir = Path(__file__).parent / "api"

    print(f"🔍 Exploration du projet: {project_root}")
    print(f"📁 Répertoire de sortie: {output_dir}")

    # Trouver tous les modules Python
    modules = find_python_modules(project_root)

    print(f"📦 {len(modules)} modules trouvés:")
    for module in modules:
        print(f"  - {module['name']}")

    # Générer les fichiers .rst pour chaque module
    print("\n📝 Génération des fichiers .rst...")
    for module in modules:
        generate_module_rst(module, output_dir)

    # Générer le fichier index
    print("\n📋 Génération du fichier index...")
    generate_index_rst(modules, output_dir)

    print(f"\n✅ Documentation générée avec succès!")
    print(f"📖 {len(modules)} modules documentés dans {output_dir}")


if __name__ == "__main__":
    main()
