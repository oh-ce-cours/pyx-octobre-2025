# Demo API - Système de gestion des utilisateurs et VMs

Ce projet est une démo API pour la gestion d'utilisateurs et de machines virtuelles avec génération de données Faker, documentation automatique et scripts utilitaires.

## 🚀 Démarrage rapide

1. **Installation des dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration de l'environnement** :
   ```bash
   cp env.example .env
   # Modifiez .env avec vos paramètres (URL API, credentails, etc.)
   ```

3. **Démarrage de l'API** :
   ```bash
   python main.py
   ```

## 📚 Scripts utilitaires

Le projet inclut plusieurs scripts Python pour vous aider dans le développement et les tests :

### 🎲 `scripts/generate_data.py` - Générateur de données factices

Génère des utilisateurs et VMs réalistes avec Faker pour les tests et démonstrations.

**Commandes disponibles :**
- `users-with-vms` : Génère des utilisateurs avec leurs VMs
- `vms-only` : Génère uniquement des VMs pour des utilisateurs existants
- `preview` : Prévisualise les données sans les sauvegarder
- `version` : Affiche la version

**Exemples d'usage :**
```bash
# Générer 50 utilisateurs avec 0-5 VMs chacun
python scripts/generate_data.py users-with-vms

# Générer 100 utilisateurs avec maximum 3 VMs
python scripts/generate_data.py users-with-vms --users 100 --max-vms 3

# Prévisualiser les données
python scripts/generate_data.py preview --users 10
```

### 🚀 `scripts/create_data_via_api.py` - Créateur de données via API

Crée des données via l'API en utilisant le générateur Faker avec gestion d'authentification et de rate limiting.

**Commandes disponibles :**
- `users` : Crée des utilisateurs via l'API
- `vms` : Crée des VMs via l'API
- `full-dataset` : Crée un dataset complet (utilisateurs + VMs)
- `status` : Affiche le statut actuel de l'API
- `version` : Affiche la version

**Exemples d'usage :**
```bash
# Créer 20 utilisateurs via l'API
python scripts/create_data_via_api.py users --count 20

# Créer 50 VMs via l'API
python scripts/create_data_via_api.py vms --count 50

# Créer un dataset complet
python scripts/create_data_via_api.py full-dataset --users 20 --vms 50

# Vérifier le statut de l'API
python scripts/create_data_via_api.py status
```

### 🧹 `scripts/quick_cleanup.py` - Script de nettoyage

Script de nettoyage pour supprimer toutes les VMs et utilisateurs avec mode simulation par défaut.

**Commandes disponibles :**
- `cleanup` : Nettoie les données (simulation par défaut)

**Exemples d'usage :**
```bash
# Mode simulation (par défaut) - aucune vérification des suppressions
python scripts/quick_cleanup.py cleanup

# Suppression réelle
python scripts/quick_cleanup.py cleanup --real

# Avec délai personnalisé entre suppressions
python scripts/quick_cleanup.py cleanup --real --delay 3
```

### 📚 `scripts/generate_docs.py` - Générateur de documentation

Génère automatiquement la documentation complète avec Sphinx et pydoc.

**Usage :**
```bash
# Générer toute la documentation
python scripts/generate_docs.py
```

Cette commande génère :
- Documentation Sphinx (HTML moderne) : `docs/sphinx/build/index.html`
- Documentation pydoc (HTML simple) : `docs/pydoc/html/index.html`

## 🏗️ Architecture du projet

```
demo_api/
├── main.py                     # Application principale FastAPI
├── vm_manager.py              # Gestionnaire des VMs
├── report_manager.py          # Gestionnaire des rapports
├── requirements.txt           # Dépendances Python
├── env.example               # Exemple de configuration d'environnement
├── utils/                     # Modules utilitaires
│   ├── api/                   # Client API et authentification
│   ├── services/              # Services métier
│   ├── data_generator.py      # Générateur de données Faker
│   └── config.py              # Configuration d'environnement
├── reports/                   # Modules de génération de rapports
│   ├── base.py                # Classe de base pour les rapports
│   ├── html_reports.py        # Rapports HTML
│   ├── json_reports.py        # Rapports JSON
│   └── markdown_reports.py    # Rapports Markdown
├── templates/                 # Templates Jinja2 pour les rapports
├── outputs/                   # Fichiers de sortie des rapports
├── scripts/                   # Scripts utilitaires
│   ├── generate_data.py       # Générateur de données
│   ├── create_data_via_api.py # Créateur de données via API
│   ├── quick_cleanup.py       # Script de nettoyage
│   └── generate_docs.py       # Générateur de documentation
└── docs/                       # Documentation
    ├── sphinx/                 # Documentation Sphinx
    └── pydoc/                  # Documentation pydoc
```

## 📋 Configuration des scripts

Tous les scripts utilisent la configuration définie dans `utils/config.py` pour :
- URL de l'API (`DEMO_API_URL`)
- Identifiants d'authentification (`DEMO_API_EMAIL`, `DEMO_API_PASSWORD`)
- Paramètres de connexion et timeout

## ⚙️ Prérequis

- Python 3.9 ou plus récent
- Dépendances installées (`pip install -r requirements.txt`)
- API démarrée et accessible
- Variables d'environnement configurées dans `.env`

## 🎯 Cas d'usage recommandés

### Scénario 1 : Tests et développement
1. Générer des données locales avec `generate_data.py`
2. Créer des données via l'API avec `create_data_via_api.py`
3. Nettoyer après les tests avec `quick_cleanup.py`

### Scénario 2 : Démonstrations
1. Créer un dataset complet : `create_data_via_api.py full-dataset --users 50 --vms 200`
2. Générer la documentation : `generate_docs.py`
3. Utiliser l'interface web pour explorer les données

### Scénario 3 : Maintenance
1. Vérifier le statut : `create_data_via_api.py status`
2. Nettoyer les données si nécessaire : `quick_cleanup.py cleanup`

## ⚠️ Notes importantes

**🚨 Sécurité** : Le script `quick_cleanup.py` peut supprimer définitivement toutes les données. Utilisez toujours le mode simulation (`--real` non spécifié) pour tester d'abord.

**💡 Conseils d'usage** :
1. Utilisez `generate_data.py` pour créer des données de test en local
2. Utilisez `create_data_via_api.py` pour les insérer dans l'API
3. Le script `create_data_via_api.py` gère automatiquement les erreurs 429 (Too Many Requests) avec retry et backoff exponentiel
4. Les délais par défaut ont été configurés pour respecter les limites de l'API

**⚡ Performance** : Le script `create_data_via_api.py` utilise des lots (`batch_size`) et des délais configurables pour optimiser les performances et éviter de surcharger l'API.

## 📖 Documentation complète

La documentation complète du projet est disponible après génération :

- **Documentation Sphinx** : Ouvrez `docs/sphinx/build/index.html` dans votre navigateur
- **Documentation pydoc** : Ouvrez `docs/pydoc/html/index.html` dans votre navigateur
- **Guide d'amélioration des barres de progression** : `docs/AMELIORATIONS_PROGRESS_BAR.md`
- **Architecture simplifiée** : `docs/ARCHITECTURE_SIMPLE.md`
- **Guide de refactoring** : `docs/REFACTORING_GUIDE.md`

## 🤝 Contribution

Pour contribuer au projet :

1. Suivez les bonnes pratiques décrites dans `docs/REFACTORING_GUIDE.md`
2. Utilisez les scripts pour générer des données de test
3. Générez la documentation après vos modifications
4. Testez vos changements avec les différents scripts utilitaires
