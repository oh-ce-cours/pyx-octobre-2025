# Documentation pdoc3

## 🚀 Génération de documentation moderne et élégante

**pdoc3** est le successeur moderne de pydoc avec une interface magnifique et CSS moderne intégré.

## ⚡ Démarrage rapide

### Serveur de développement
```bash
# Documenter tous les modules principaux
pdoc --http :8080 main report_manager utils.config

# Documenter un module spécifique
pdoc --http :8080 main

# Documenter tout le package
pdoc --http :8080 .
```

### Génération statique
```bash
# Générer des fichiers HTML
pdoc --html main report_manager

# Générer avec répertoire de sortie
pdoc --html -o docs/html main report_manager
```

## 🎨 Caractéristiques

- ✅ **CSS moderne** intégré avec highlight.js
- ✅ **Design responsive** et professionnel
- ✅ **Navigation interactive** avec sidebar
- ✅ **Syntaxe highlighting** automatique
- ✅ **Documentation markdown** dans les docstrings
- ✅ **Serveur intégré** automatique
- ✅ **Auto-découverte** des modules

## 📖 Accès

- **Serveur développement** : http://localhost:8080
- **Modules disponibles** :
  - http://localhost:8080/main/
  - http://localhost:8080/report_manager/
  - http://localhost:8080/utils.config/

## 🔧 Intégration avec scripts

Pour intégrer dans le workflow de génération de docs :
