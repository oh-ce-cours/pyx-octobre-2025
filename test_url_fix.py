#!/usr/bin/env python3
"""
Script de test pour vérifier la correction des URLs statiques.
"""

import re

def test_url_corrections():
    """Teste la correction des URLs pour GitHub Pages."""
    
    # Simuler le contenu HTML avec des chemins incorrects
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
    
    base_url = "https://oh-ce-cours.github.io/pyx-octobre-2025/sphinx"
    
    # Patterns de correction (version corrigée)
    patterns = [
        # Chemins directs _static/ vers chemins absolus avec static/ (sans underscore)
        (r'href="_static/', f'href="{base_url}/static/'),
        (r'src="_static/', f'src="{base_url}/static/'),
        (r'url\("_static/', f'url("{base_url}/static/'),
        (r"url\('_static/", f"url('{base_url}/static/"),
        # Chemins relatifs ../_static/ vers chemins absolus avec static/
        (r'href="../_static/', f'href="{base_url}/static/'),
        (r'src="../_static/', f'src="{base_url}/static/'),
        (r'url\("../_static/', f'url("{base_url}/static/'),
        (r"url\('../_static/", f"url('{base_url}/static/"),
        # Chemins relatifs ./_static/ vers chemins absolus avec static/
        (r'href="./_static/', f'href="{base_url}/static/'),
        (r'src="./_static/', f'src="{base_url}/static/'),
        (r'url\("./_static/', f'url("{base_url}/static/'),
        (r"url\('./_static/", f"url('{base_url}/static/"),
        # Patterns spécifiques pour les fichiers CSS dans le HTML
        (r'<link[^>]*href="_static/', f'<link href="{base_url}/static/'),
        (r'<script[^>]*src="_static/', f'<script src="{base_url}/static/'),
        # Patterns pour les imports CSS dans les fichiers CSS
        (r'@import\s+"_static/', f'@import "{base_url}/static/'),
        (r"@import\s+'_static/", f"@import '{base_url}/static/"),
    ]
    
    # Appliquer les corrections
    corrected_html = test_html
    for pattern, replacement in patterns:
        corrected_html = re.sub(pattern, replacement, corrected_html)
    
    print("🔍 Test de correction des URLs statiques")
    print("=" * 60)
    print("📝 HTML original:")
    print(test_html)
    print("\n✅ HTML corrigé:")
    print(corrected_html)
    
    # Vérifier que les corrections ont été appliquées
    expected_patterns = [
        f'href="{base_url}/static/pygments.css',
        f'href="{base_url}/static/styles/furo.css',
        f'src="{base_url}/static/scripts/furo.js',
        f'src="{base_url}/static/file.png',
        f"url('{base_url}/static/plus.png')"
    ]
    
    print("\n🔍 Vérification des corrections:")
    all_fixed = True
    for pattern in expected_patterns:
        if pattern in corrected_html:
            print(f"✅ {pattern}")
        else:
            print(f"❌ Manquant: {pattern}")
            all_fixed = False
    
    print(f"\n📊 Résultat: {'🎉 Toutes les corrections appliquées!' if all_fixed else '⚠️  Certaines corrections manquantes'}")
    
    # Vérifier que l'URL ne contient plus "docs-deploy"
    if "docs-deploy" not in corrected_html:
        print("✅ URL corrigée: plus de 'docs-deploy' dans les chemins")
    else:
        print("❌ Problème: 'docs-deploy' encore présent dans les chemins")
        all_fixed = False
    
    # Vérifier que les chemins utilisent "static" au lieu de "_static"
    if "_static/" not in corrected_html:
        print("✅ Chemins corrigés: utilisation de 'static/' au lieu de '_static/'")
    else:
        print("❌ Problème: '_static/' encore présent dans les chemins")
        all_fixed = False
    
    return all_fixed

if __name__ == "__main__":
    test_url_corrections()
