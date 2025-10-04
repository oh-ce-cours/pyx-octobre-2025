#!/bin/bash

echo "🚀 Script de déploiement manuel pour GitHub Pages"
echo "=" * 50

# Se placer dans le bon répertoire
cd tape_en_cours/demo_api

# Générer la documentation
echo "📚 Génération de la documentation..."
python scripts/generate_docs.py

# Créer le dossier de déploiement
echo "📁 Préparation des fichiers pour GitHub Pages..."
cd ../../
mkdir -p docs-deploy/sphinx
mkdir -p docs-deploy/pdoc3
cp -r tape_en_cours/demo_api/docs/sphinx/build/* docs-deploy/sphinx/
cp -r tape_en_cours/demo_api/docs/pdoc3/* docs-deploy/pdoc3/

# Créer une copie du dossier _static en static pour GitHub Pages
echo "📁 Création d'une copie static/ pour GitHub Pages..."
if [ -d "docs-deploy/sphinx/_static" ]; then
    cp -r docs-deploy/sphinx/_static docs-deploy/sphinx/static
    echo "✅ Dossier static/ créé à partir de _static/"
else
    echo "⚠️  Dossier _static non trouvé"
fi

# Les fichiers statiques restent dans leurs dossiers respectifs

# Ajouter les fichiers nécessaires pour GitHub Pages
touch docs-deploy/.nojekyll
echo "✅ Fichier .nojekyll créé pour désactiver Jekyll sur GitHub Pages"

# Créer un fichier robots.txt pour éviter l'indexation des fichiers de build
cat > docs-deploy/robots.txt << 'EOF'
User-agent: *
Allow: /
Disallow: /_static/
Disallow: /_sources/
EOF
echo "✅ Fichier robots.txt créé"

# Corriger les chemins CSS dans tous les fichiers HTML pour GitHub Pages
echo "🔧 Correction des chemins CSS pour GitHub Pages..."
BASE_URL="https://oh-ce-cours.github.io/pyx-octobre-2025/docs-deploy"

# Fonction pour corriger les chemins CSS de manière propre
fix_css_paths() {
    local file="$1"
    local relative_path=""
    
    # Déterminer le chemin relatif selon le dossier
    if [[ "$file" == *"/sphinx/"* ]]; then
        relative_path="${BASE_URL}/sphinx"
    elif [[ "$file" == *"/pdoc3/"* ]]; then
        relative_path="${BASE_URL}/pdoc3"
    else
        relative_path="${BASE_URL}"
    fi
    
    echo "🔧 Correction des chemins dans: $file"
    echo "   Base URL: $relative_path"
    
    # Détecter le système d'exploitation pour la compatibilité sed
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' \
            -e "s|href=\"_static/|href=\"${relative_path}/static/|g" \
            -e "s|src=\"_static/|src=\"${relative_path}/static/|g" \
            -e "s|url(\"_static/|url(\"${relative_path}/static/|g" \
            -e "s|url('_static/|url('${relative_path}/static/|g" \
            -e "s|href=\"../_static/|href=\"${relative_path}/static/|g" \
            -e "s|src=\"../_static/|src=\"${relative_path}/static/|g" \
            -e "s|url(\"../_static/|url(\"${relative_path}/static/|g" \
            -e "s|url('../_static/|url('${relative_path}/static/|g" \
            "$file"
    else
        # Linux/Unix
        sed -i \
            -e "s|href=\"_static/|href=\"${relative_path}/static/|g" \
            -e "s|src=\"_static/|src=\"${relative_path}/static/|g" \
            -e "s|url(\"_static/|url(\"${relative_path}/static/|g" \
            -e "s|url('_static/|url('${relative_path}/static/|g" \
            -e "s|href=\"../_static/|href=\"${relative_path}/static/|g" \
            -e "s|src=\"../_static/|src=\"${relative_path}/static/|g" \
            -e "s|url(\"../_static/|url(\"${relative_path}/static/|g" \
            -e "s|url('../_static/|url('${relative_path}/static/|g" \
            "$file"
    fi
}

# Appliquer la correction à tous les fichiers HTML (Sphinx et pdoc3)
find docs-deploy -name "*.html" -type f | while read -r file; do
    fix_css_paths "$file"
done

# Appliquer la correction aux fichiers CSS également
find docs-deploy -name "*.css" -type f | while read -r file; do
    fix_css_paths "$file"
done

# Appliquer la correction aux fichiers JS également
find docs-deploy -name "*.js" -type f | while read -r file; do
    fix_css_paths "$file"
done

echo "✅ Chemins CSS corrigés pour GitHub Pages"

# Créer une page d'accueil avec navigation
cat > docs-deploy/index.html << 'EOF'
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PYx - Documentation Python Avancé</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 40px; }
        .section { margin: 30px 0; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; }
        .btn { display: inline-block; padding: 12px 24px; background: #007acc; color: white; text-decoration: none; border-radius: 6px; margin: 10px 10px 0 0; }
        .btn:hover { background: #005999; }
        .info { background: #f0f8ff; padding: 15px; border-radius: 6px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐍 PYx - Formation Python Avancé</h1>
            <p>Documentation complète du projet pédagogique Python</p>
        </div>

        <div class="info">
            <h3>📚 Documentation principale</h3>
            <p>Choisissez la version qui correspond le mieux à vos besoins :</p>
            
            <a href="./sphinx/index.html" class="btn">📖 Sphinx (Complète)</a>
            <a href="./pdoc3/index.html" class="btn">⚡ pdoc3 (Moderne)</a>
        </div>

        <div class="section">
            <h3>🎯 Modules disponibles</h3>
            <ul>
                <li><a href="./sphinx/api/index.html">🔧 API Reference</a> - Documentation complète de l'API</li>
                <li><a href="./sphinx/examples.html">💡 Exemples</a> - Code d'exemple et cas d'usage</li>
                <li><a href="./sphinx/cli/index.html">⚡ Interface CLI</a> - Commandes disponibles</li>
            </ul>
        </div>

        <div class="section">
            <h3>🚀 Demo API - Fonctionnel et disponible !</h3>
            <p>L'API de démonstration est entièrement opérationnelle avec :</p>
            <ul>
                <li>Authentification sécurisée</li>
                <li>Gestion de machines virtuelles</li>
                <li>Génération de rapports</li>
                <li>Interface CLI moderne avec Typer</li>
            </ul>
            <p><strong>👨‍🎓 Parfait pour les étudiants !</strong></p>
        </div>

        <div class="section">
            <h3>🔧 Instructions de développement</h3>
            <pre><code># Clone le repository
git clone https://github.com/yourusername/pyx-octobre-2025.git
cd pyx-octobre-2025

# Aller dans demo_api
cd tape_en_cours/demo_api

# Installer les dépendances
pip install -r requirements.txt

# Tester l'API
python main.py --help
python main.py version</code></pre>
        </div>
    </div>
</body>
</html>
EOF

echo "✅ Déploiement préparé !"
echo ""
echo "📋 Prochaines étapes :"
echo "   1. git add docs-deploy/"
echo "   2. git commit -m 'Deploy documentation to GitHub Pages'"
echo "   3. git push origin main"
echo ""
echo "🌐 Après push, GitHub Pages sera disponible sur :"
echo "   https://oh-ce-cours.github.io/pyx-octobre-2025/"
