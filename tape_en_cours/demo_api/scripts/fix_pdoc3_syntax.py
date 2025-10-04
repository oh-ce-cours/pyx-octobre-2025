#!/usr/bin/env python3
"""
Script de refactoring pour corriger la syntaxe des blocs de code shell
compatible avec pdoc3.

Problème : pdoc3 interprète mal les blocs .. code-block:: shell
Solution : Conversion vers la syntaxe Markdown compatible
"""

import re
import os
from pathlib import Path
from typing import List, Tuple


def find_code_blocks(content: str) -> List[Tuple[int, int, str]]:
    """
    Trouve tous les blocs .. code-block:: shell dans le contenu.

    Returns:
        List de tuples (start, end, block_content)
    """
    pattern = r"\.\. code-block:: shell\n\n((?:        .*\n?)*)"
    matches = []

    for match in re.finditer(pattern, content, re.MULTILINE):
        start = match.start()
        end = match.end()
        block_content = match.group(1)
        matches.append((start, end, block_content))

    return matches


def convert_code_block(block_content: str) -> str:
    """
    Convertit un bloc de code shell en syntaxe Markdown.

    Args:
        block_content: Le contenu du bloc de code (avec indentation)

    Returns:
        Le bloc converti en Markdown
    """
    # Supprimer l'indentation de 8 espaces
    lines = block_content.split("\n")
    cleaned_lines = []

    for line in lines:
        if line.strip():  # Ignorer les lignes vides
            # Supprimer les 8 premiers espaces
            if line.startswith("        "):
                cleaned_lines.append(line[8:])
            else:
                cleaned_lines.append(line)
        else:
            cleaned_lines.append("")

    # Rejoindre et créer le bloc Markdown
    code_lines = "\n".join(cleaned_lines)
    return f"```shell\n{code_lines}\n```"


def fix_file(file_path: Path) -> bool:
    """
    Corrige la syntaxe des blocs de code dans un fichier.

    Args:
        file_path: Chemin vers le fichier à corriger

    Returns:
        True si des modifications ont été apportées
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Trouver tous les blocs code-block:: shell
        code_blocks = find_code_blocks(content)

        if not code_blocks:
            return False

        print(f"  📝 {len(code_blocks)} bloc(s) trouvé(s) dans {file_path.name}")

        # Convertir de la fin vers le début pour éviter les problèmes d'index
        for start, end, block_content in reversed(code_blocks):
            markdown_block = convert_code_block(block_content)
            content = content[:start] + markdown_block + content[end:]

        # Sauvegarder le fichier modifié
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return True

    except Exception as e:
        print(f"  ❌ Erreur lors du traitement de {file_path}: {e}")
        return False


def main():
    """Fonction principale."""
    print("🔧 Refactoring de la syntaxe des blocs de code pour pdoc3")
    print("=" * 60)

    # Répertoire du projet
    project_root = Path(__file__).parent.parent
    print(f"📁 Répertoire du projet: {project_root}")

    # Fichiers Python à traiter
    python_files = [
        "main.py",
        "vm_manager.py",
        "report_manager.py",
        "scripts/generate_data.py",
        "scripts/create_data_via_api.py",
    ]

    modified_count = 0
    total_files = len(python_files)

    for file_path in python_files:
        full_path = project_root / file_path

        if not full_path.exists():
            print(f"⚠️  Fichier non trouvé: {file_path}")
            continue

        print(f"\n🔍 Traitement de {file_path}...")

        if fix_file(full_path):
            modified_count += 1
            print(f"  ✅ Fichier modifié avec succès")
        else:
            print(f"  ℹ️  Aucun bloc code-block:: shell trouvé")

    print("\n" + "=" * 60)
    print(f"📊 Résumé: {modified_count}/{total_files} fichiers modifiés")

    if modified_count > 0:
        print("\n🎉 Refactoring terminé!")
        print("\n📖 Prochaines étapes:")
        print("1. Tester la génération pdoc3: pdoc --html -o docs/pdoc3 . --force")
        print("2. Vérifier que les blocs de code s'affichent correctement")
        print("3. Régénérer la documentation complète si nécessaire")
    else:
        print("\nℹ️  Aucun fichier n'a nécessité de modification")


if __name__ == "__main__":
    main()
