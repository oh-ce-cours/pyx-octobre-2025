# Documentation pdoc3 - Demo API

## 🚀 Documentation moderne auto-générée

Ce répertoire contient la documentation complète générée avec **pdoc3**, incluant un **index principal** pour faciliter la navigation.

## ⚡ Navigation

### Accès direct
- **Index principal** : [`index.html`](./index.html) - Navigation complète vers tous les modules
- **Module demo_api** : [`demo_api/index.html`](./demo_api/index.html) - Documentation principale

### Flux de documentation
```
index.html                    ← Point d'entrée principal
├── demo_api/index.html       ← Module principal  
├── demo_api/main.html        ← Application FastAPI
├── demo_api/scripts/         ← Scripts utilitaires
├── demo_api/utils/           ← Modules utilitaires  
└── demo_api/reports/         ← Génération de rapports
```

## 🔧 Génération

### Automatique (recommandée)
```bash
python scripts/generate_docs.py
```

### Manuelle
```bash
# Génération statique complète
pdoc --html -o docs/pdoc3 . --force

# Serveur de développement  
pdoc --http :8080 .
```

## 💡 Fonctionnalités

### Index personnalisé
- 🌟 **Navigation organisée** par catégories
- 🔗 **Liens directs** vers tous les modules principaux  
- 📚 **Guide d'utilisation** intégré
- 🎨 **Interface moderne** avec CSS intégré

### Auto-génération
- 📖 **Documentation automatique** depuis les docstrings Python
- 🔍 **Syntaxe highlighting** automatique
- 📱 **Design responsive** et mobile-friendly
- ⚡ **Mise à jour** automatique lors de chaque génération

## 📖 Modules disponibles

| Module | Description |
|--------|-------------|
| `main` | 🎮 Application principale FastAPI |
| `report_manager` | 📊 Gestionnaire des rapports |
| `vm_manager` | 🖥️ Gestionnaire des VMs |
| `scripts/` | 🔨 Scripts de développement |
| `utils/` | ⚙️ Modules utilitaires |
| `reports/` | 📈 Génération de rapports |

## 🚀 Pour le développement

**Mode serveur (recommandé)** :
```bash
pdoc --http :8080 . --open-browser
# Accès automatique à : http://localhost:8080
```

**Mode statique** :
```bash  
pdoc --html -o docs/pdoc3 . --force
# Ouvrir : docs/pdoc3/index.html
```

## ✨ Avantages vs autres outils

- ✅ **Plus simple** que Sphinx
- ✅ **Auto-génération** depuis docstrings
- ✅ **CSS moderne** intégré
- ✅ **Serveur intégré** pour développement
- ✅ **Index personnalisé** pour navigation optimisée
