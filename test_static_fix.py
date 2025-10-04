#!/usr/bin/env python3
"""
Script de test pour vérifier la correction des chemins statiques.
"""

import os
import re
from pathlib import Path

def test_static_path_fix():
    """Teste la correction des chemins statiques."""
    
    # Simuler le contenu HTML avec des chemins relatifs
    test_html = '''<!doctype html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="_static/pygments.css?v=acfd86a5" />
    <link rel="stylesheet" type="text/css" href="_static/styles/furo.css?v=580074bf" />
    <script src="_static/scripts/furo.js"></script>
    <img src="_static/file.png" alt="test" />
</head>
<body>
    <div style="background: url('_static/plus.png')"></div>
</body>
</html>'''
    
    base_url = "https://oh-ce-cours.github.io/pyx-octobre-2025/docs-deploy/sphinx"
    
    # Patterns de correction
    patterns = [
        # Chemins directs _static/ vers chemins absolus
        (r'href="_static/', f'href="{base_url}/_static/'),
        (r'src="_static/', f'src="{base_url}/_static/'),
        (r'url\("_static/', f'url("{base_url}/_static/'),
        (r"url\('_static/", f"url('{base_url}/_static/"),
        
        # Chemins relatifs ../_static/ vers chemins absolus
        (r'href="../_static/', f'href="{base_url}/_static/'),
        (r'src="../_static/', f'src="{base_url}/_static/'),
        (r'url\("../_static/', f'url("{base_url}/_static/'),
        (r"url\('../_static/", f"url('{base_url}/_static/"),
        
        # Chemins relatifs ./_static/ vers chemins absolus
        (r'href="./_static/', f'href="{base_url}/_static/'),
        (r'src="./_static/', f'src="{base_url}/_static/'),
        (r'url\("./_static/', f'url("{base_url}/_static/'),
        (r"url\('./_static/", f"url('{base_url}/_static/"),
        
        # Patterns spécifiques pour les fichiers CSS dans le HTML
        (r'<link[^>]*href="_static/', f'<link href="{base_url}/_static/'),
        (r'<script[^>]*src="_static/', f'<script src="{base_url}/_static/'),
        
        # Patterns pour les imports CSS dans les fichiers CSS
        (r'@import\s+"_static/', f'@import "{base_url}/_static/'),
        (r"@import\s+'_static/", f"@import '{base_url}/_static/"),
    ]
    
    # Appliquer les corrections
    corrected_html = test_html
    for pattern, replacement in patterns:
        corrected_html = re.sub(pattern, replacement, corrected_html)
    
    print("🔍 Test de correction des chemins statiques")
    print("=" * 50)
    print("📝 HTML original:")
    print(test_html)
    print("\n✅ HTML corrigé:")
    print(corrected_html)
    
    # Vérifier que les corrections ont été appliquées
    expected_patterns = [
        f'href="{base_url}/_static/pygments.css',
        f'href="{base_url}/_static/styles/furo.css',
        f'src="{base_url}/_static/scripts/furo.js',
        f'src="{base_url}/_static/file.png',
        f"url('{base_url}/_static/plus.png')"
    ]
    
    all_fixed = True
    for pattern in expected_patterns:
        if pattern not in corrected_html:
            print(f"❌ Pattern manquant: {pattern}")
            all_fixed = False
    
    if all_fixed:
        print("\n🎉 Tous les chemins ont été corrigés avec succès!")
    else:
        print("\n⚠️  Certains chemins n'ont pas été corrigés")
    
    return all_fixed

if __name__ == "__main__":
    test_static_path_fix()
