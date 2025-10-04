# Documentation Demo API

Ce répertoire contient toute la documentation du projet Demo API, générée automatiquement avec Sphinx et pydoc.

## Structure

```
docs/
├── README.md                    # Ce fichier
├── sphinx/                      # Documentation Sphinx
│   ├── source/                  # Sources de documentation
│   │   ├── conf.py             # Configuration Sphinx
│   │   ├── index.rst           # Page d'accueil
│   │   ├── generate_modules.py # Script d'auto-découverte
│   │   └── api/                # Documentation des modules
│   └── build/                   # Documentation générée (HTML)
└── pydoc/                       # Documentation pydoc
    ├── generate_pydoc.py        # Script de génération pydoc
    └── html/                    # Documentation générée (HTML)
```

## Génération de la documentation

### Méthode automatique (recommandée)

Utilisez le script de génération complet :

```bash
python scripts/generate_docs.py
```

Ce script :
1. Découvre automatiquement tous les modules Python
2. Génère la documentation Sphinx
3. Génère la documentation pydoc

### Méthode manuelle

#### Documentation Sphinx

1. **Auto-découverte des modules** :
   ```bash
   python docs/sphinx/source/generate_modules.py
   ```

2. **Génération de la documentation** :
   ```bash
   cd docs/sphinx
   sphinx-build -b html source build
   ```

3. **Accès à la documentation** :
   Ouvrez `docs/sphinx/build/index.html` dans votre navigateur

#### Documentation pydoc

1. **Génération de la documentation** :
   ```bash
   python docs/pydoc/generate_pydoc.py
   ```

2. **Accès à la documentation** :
   Ouvrez `docs/pydoc/html/index.html` dans votre navigateur

## Fonctionnalités

### Auto-découverte

- **Découverte automatique** : Tous les modules Python sont automatiquement découverts
- **Exclusion intelligente** : Les dossiers `__pycache__`, `.git`, `docs`, etc. sont exclus
- **Structure préservée** : La hiérarchie des modules est respectée

### Sphinx

- **Thème moderne** : Utilise le thème Read the Docs
- **Support des types** : Affichage des annotations de type
- **Navigation** : Index et recherche intégrés
- **Multi-format** : Support HTML, PDF, etc.

### pydoc

- **Documentation simple** : Documentation HTML basique mais complète
- **Navigation** : Index avec liens vers tous les modules
- **Style personnalisé** : Interface claire et lisible

## Personnalisation

### Ajouter des modules

Les nouveaux modules Python sont automatiquement découverts lors de la prochaine génération.

### Modifier la configuration Sphinx

Éditez `docs/sphinx/source/conf.py` pour :
- Changer le thème
- Ajouter des extensions
- Modifier les paramètres d'autodoc

### Personnaliser pydoc

Éditez `docs/pydoc/generate_pydoc.py` pour :
- Modifier le style CSS
- Changer la structure de l'index
- Ajouter des métadonnées

## Dépendances

Les dépendances suivantes sont requises :

```txt
sphinx>=7.1.2
sphinx-rtd-theme>=2.0.0
sphinx-autodoc-typehints>=1.25.0
myst-parser>=2.0.0
```

Installez-les avec :

```bash
pip install -r requirements.txt
```

## Intégration CI/CD

Pour intégrer la génération de documentation dans votre pipeline CI/CD :

```yaml
# Exemple GitHub Actions
- name: Generate Documentation
  run: python scripts/generate_docs.py

- name: Deploy Documentation
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./docs/sphinx/build
```
