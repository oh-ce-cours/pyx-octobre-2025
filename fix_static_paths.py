#!/usr/bin/env python3
"""
Script pour corriger les chemins _static vers static dans les fichiers HTML/CSS/JS.
Remplace les commandes sed pour une meilleure compatibilité cross-platform.
"""

import os
import re
import sys
from pathlib import Path


def fix_static_paths(file_path: str, base_url: str) -> bool:
    """
    Corrige les chemins _static vers static dans un fichier.
    
    Args:
        file_path: Chemin vers le fichier à corriger
        base_url: URL de base pour les chemins absolus
        
    Returns:
        True si des modifications ont été apportées, False sinon
    """
    try:
        # Lire le fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
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


def get_relative_path(file_path: str, base_dir: str) -> str:
    """
    Calcule le chemin relatif pour construire l'URL de base.
    
    Args:
        file_path: Chemin du fichier
        base_dir: Répertoire de base (docs-deploy)
        
    Returns:
        URL de base pour les chemins
    """
    file_path = Path(file_path)
    base_path = Path(base_dir)
    
    # Calculer la profondeur relative
    try:
        relative_path = file_path.relative_to(base_path)
        depth = len(relative_path.parts) - 1  # -1 car on ne compte pas le fichier lui-même
        
        if depth == 0:
            # Fichier à la racine de docs-deploy
            return "https://oh-ce-cours.github.io/pyx-octobre-2025/docs-deploy"
        elif depth == 1:
            # Fichier dans un sous-dossier (ex: sphinx/, pdoc3/)
            subfolder = relative_path.parts[0]
            return f"https://oh-ce-cours.github.io/pyx-octobre-2025/docs-deploy/{subfolder}"
        else:
            # Fichier plus profond
            subfolder = relative_path.parts[0]
            return f"https://oh-ce-cours.github.io/pyx-octobre-2025/docs-deploy/{subfolder}"
    except ValueError:
        # Si le fichier n'est pas dans base_dir, utiliser l'URL par défaut
        return "https://oh-ce-cours.github.io/pyx-octobre-2025/docs-deploy"


def main():
    """Fonction principale."""
    if len(sys.argv) != 2:
        print("Usage: python fix_static_paths.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    base_dir = "docs-deploy"
    
    if not os.path.exists(file_path):
        print(f"❌ Fichier non trouvé: {file_path}")
        sys.exit(1)
    
    # Calculer l'URL de base
    base_url = get_relative_path(file_path, base_dir)
    
    print(f"🔧 Correction des chemins dans: {file_path}")
    print(f"   Base URL: {base_url}")
    
    # Corriger les chemins
    success = fix_static_paths(file_path, base_url)
    
    if success:
        print("✅ Correction terminée avec succès")
        sys.exit(0)
    else:
        print("⚠️  Aucune correction nécessaire")
        sys.exit(0)


if __name__ == "__main__":
    main()
