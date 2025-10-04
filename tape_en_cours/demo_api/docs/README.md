# Documentation Demo API

Ce répertoire contient toute le documentation du projet Demo API, générée automatiquement avec **Sphinx** et **pdoc3**.

## 🎯 Outils de Documentation

### 📚 Sphinx (Complexe mais puissant)
- **Documentation approfondie** pour utilisateurs finaux
- **Thème Read the Docs** professionnel
- **Recherche intégrée** et navigation avancée
- **Support multi-format** (HTML, PDF, etc.)

### ⚡ pdoc3 (Simple et moderne)
- **Interface moderne** avec CSS intégré
- **Syntaxe highlighting** automatique
- **Serveur de développement** rapide
- **Auto-génération** depuis les docstrings

## 🚀 Génération de la Documentation

### Méthode Automatisée (Recommandée)

```bash
# Génération complète
python scripts/generate_docs.py
```

Ce script génère :
1. **Sphinx** : Documentation complète avec thème professionnel
2. **pdoc3** : Documentation moderne avec CSS intégré

### Méthode Manuelle

#### Documentation Sphinx
```bash
# Auto-découverte des modules
python docs/sphinx/source/generate_modules.py

# Génération HTML
cd docs/sphinx
sphinx-build -b html source build
```

#### Documentation pdoc3
```bash
# Serveur de développement (recommandé)
pdoc --http :8080 main report_manager utils.config

# Génération statique HTML
pdoc --html -o docs/pdoc3_html main report_manager
```

## 📖 Accès à la Documentation

### Développement quotidien
- **pdoc3** : http://localhost:8080 (serveur automatique)
- **Moderne et rapide** avec CSS intégré

### Documentation finale
- **Sphinx** : `docs/sphinx/build/index.html`
- **Complète** avec thème professionnel

## 🔧 Structure des Fichiers

```
docs/
├── README.md                    # Ce fichier
├── sphinx/                      # Documentation Sphinx
│   ├── source/                  # Sources de documentation
│   │   ├── conf.py             # Configuration Sphinx
│   │   ├── generate_modules.py # Auto-découverte
│   │   └── api/                # Documentation des modules
│   └── build/                   # Documentation générée (HTML)
├── pdoc3/                       # Documentation pdoc3
│   ├── README.md               # Guide pdoc3
│   └── serve_pdoc3.py         # Script serveur
└── pdoc3_html/                  # Documentation pdoc3 générée
```

## ✨ Fonctionnalités

### Auto-découverte
- **Découverte automatique** de tous les modules Python
- **Exclusion intelligente** des dossiers non pertinents
- **Structure hiérarchique** préservée

### Moderne et Professionnel
- **CSS moderne** avec highlight.js intégré
- **Design responsive** et mobile-friendly
- **Navigation interactive** avec sidebar
- **Syntaxe highlighting** automatique Python

### Intégration CI/CD
- **Scripts automatisés** pour génération
- **Prêt pour déploiement** automatique
- **Support multi-environnement**

## 🛠️ Dépendances

```txt
# Documentation
sphinx>=7.1.2
sphinx-rtd-theme>=2.0.0
sphinx-autodoc-typehints>=1.25.0
myst-parser>=2.0.0
pdoc3>=0.10.0
```

Installation :
```bash
pip install -r requirements.txt
```

## 💡 Recommandations d'Usage

### Pour le développement
```bash
# Lancez simplement le serveur pdoc3
pdoc --http :8080 main utils.config
```

### Pour la documentation
```bash
# Générez tout automatiquement
python scripts/generate_docs.py
```

## 🔄 Migration depuis pydoc

- ❌ ~Supprimé~ : Scripts pydoc complexes
- ✅ **Nouveau** : pdoc3 avec CSS moderne intégré
- ✅ **Gardé** : Sphinx pour documentation approfondie