# Guide d'utilisation pour demo_api

## Fonctionnalités

- ✓ Gestion sécurisée des mots de passe avec variables d'environnement et saisie interactive
- ✓ Logging structuré avec structlog pour debugging et monitoring
- ✓ API unifiée pour les utilisateurs et VMs
- ✓ Sauvegarde automatique en JSON des données récupérées

## Installation des dépendances

```bash
pip install -r requirements.txt
```

## Configuration centralisée

Le projet utilise maintenant un système de configuration centralisée avec `python-dotenv` qui gère automatiquement tous les paramètres de l'application.

### Variables d'environnement disponibles

Le système de configuration gère les variables d'environnement suivantes :

### Variables disponibles

#### **Configuration API :**
- `DEMO_API_BASE_URL` : URL de base de l'API (défaut: https://x8ki-letl-twmt.n7.xano.io/api:N1uLlTBt)
- `DEMO_API_TIMEOUT` : Timeout des requêtes en secondes (défaut: 5)
- `DEMO_API_MAX_RETRIES` : Nombre de tentatives en cas d'échec (défaut: 3)

#### **Authentification :**
- `DEMO_API_EMAIL` : Email pour se connecter à l'API
- `DEMO_API_PASSWORD` : Mot de passe pour se connecter à l'API
- `DEMO_API_TOKEN` : Token d'authentification (optionnel - créé automatiquement)

#### **Logging :**
- `DEMO_API_DEBUG` : Active le mode debug (true/false)
- `DEMO_API_LOG_LEVEL` : Niveau de logging (DEBUG, INFO, WARNING, ERROR)

#### **Fichiers :**
- `DEMO_API_OUTPUT_FILE` : Nom du fichier de sortie JSON (défaut: vm_users.json)

### Configuration

1. **Via les variables d'environnement** (recommandé pour la production) :
   ```bash
   export DEMO_API_EMAIL="jean@dupont21.com"
   export DEMO_API_PASSWORD="motdepasse_securise"
   python main.py
   ```

2. **Via un fichier .env** (vous pouvez utiliser python-dotenv si nécessaire) :
   ```bash
   # Créer un fichier .env
   echo "DEMO_API_EMAIL=jean@dupont21.com" >> .env
   echo "DEMO_API_PASSWORD=motdepasse_securise" >> .env
   ```

3. **Saisie interactive** (si aucune variable d'environnement) :
   Le script demandera automatiquement la saisie sécurisée du mot de passe.

### Sécurité

- Les mots de passe ne sont jamais affichés en claire
- La saisie interactive utilise `getpass` qui masque la saisie
- Les variables d'environnement permettent d'éviter les mots de passe en dur dans le code
- Ne jamais committer de fichiers .env dans le versioning

### Fonctionnement

Le code vérifie d'abord les variables d'environnement, puis demande une saisie interactive si celles-ci ne sont pas définies.

## Logging avec structlog

Le système utilise `structlog` pour un logging structuré et professionnel :

### Configuration automatique
- Logging avec couleurs dans le terminal
- Format JSON en production
- Monitoring des performances des API calls
- Gestion d'erreurs détaillée

### Exemples de logs générés
```
2024-01-15T10:30:45Z INFO D'but de l'excution de demo_api base_url=https://x8ki-letl-twmt.n7.xano.io/api:N1uLlTBt
2024-01-15T10:30:45Z INFO R'cupëration des utilisateurs depuis l'API base_url=https://x8ki-letl-twmt.n7.xano.io/api:N1uLlTBt
2024-01-15T10:30:46Z INFO Utilisateurs r'cupërés count=15 status_code=200
```

### Utilisation

```bash
# Mode développement avec logs détaillés
DEMO_API_DEBUG=true python main.py

# Mode production avec logs minimaux
DEMO_API_LOG_LEVEL=WARNING python main.py

# Logs seulement les erreurs et avertissements
DEMO_API_LOG_LEVEL=WARNING python main.py
```

### Avantages du logging structuré

- **Debugging facile** : Recherche rapide des erreurs par email, user_id, etc.
- **Monitoring** : Suivi des performances et des erreurs
- **Audit** : Traçabilité complète des actions utilisateurs
- **Production-ready** : Format adapté aux systèmes de monitoring

## Gestion intelligente des tokens d'authentification

Le système dispose de fonctions avancées pour gérer les tokens d'authentification :

### Fonctions spécialisées par type d'accès

#### **Variables d'environnement :**
- `get_token_from_env()` : Récupère un token depuis les variables d'environnement
- `save_token_to_env()` : Sauvegarde un token dans les variables d'environnement
- `remove_token_from_env()` : Supprime un token des variables d'environnement

#### **Fichiers .env avec python-dotenv :**
- `save_token_to_env_file()` : Sauvegarde un token dans un fichier .env
- `load_token_from_env_file()` : Charge un token depuis un fichier .env
- `load_env_files()` : Charge automatiquement plusieurs fichiers .env

#### **Gestion intelligente :**
- `get_or_create_token()` : Fonction tout-en-un qui essaie de récupérer un token existant ou en crée un nouveau

### Utilisation recommandée

```python
from utils.password_utils import get_or_create_token

# Utilisation simple - gère automatiquement tout
token = get_or_create_token(
    base_url="https://api.example.com",
    email="user@example.com",
    token_env_var="DEMO_API_TOKEN"
)
```

### Avantages de cette approche

- **🚀 Performance** : Réutilise les tokens valides sans nouvelle authentification
- **🔒 Sécurité** : Validation automatique des tokens avant utilisation
- **💾 Persistance** : Sauvegarde entre les sessions pour éviter les reconnexions
- **🔄 Flexibilité** : Support des variables d'environnement ET des fichiers .env
- **🛡️ Robustesse** : Gestion automatique des tokens expirés

### Scénarios d'usage

1. **Première exécution** : Demande les identifiants, crée et sauvegarde le token
2. **Exécutions suivantes** : Utilise le token sauvegardé (plus rapide)
3. **Token expiré** : Détecte automatiquement et recrée un nouveau token
4. **Environnement de production** : Utilise uniquement les tokens des variables d'environnement

## Utilisation de la configuration centralisée

### Import et configuration

```python
from utils.config import config

# Accès direct aux propriétés
base_url = config.DEMO_API_BASE_URL
timeout = config.DEMO_API_TIMEOUT
debug_mode = config.DEMO_API_DEBUG
```

### Propriétés pratiques

```python
# Vérification de l'environnement
if config.is_production:
    print("Mode production activé")

# Vérification des identifiants
if config.has_credentials:
    print("Identifiants disponibles")

# Headers d'authentification automatiques
headers = config.auth_headers
if headers:
    api_call(url, headers=headers)

# Configuration client complète
client_config = config.client_config
# {'base_url': '...', 'timeout': 5, 'max_retries': 3, 'ssl_verify': True}
```

### Validation automatique

Les configurations sont automatiquement validées au démarrage :
- URL valide (commence par `http`)
- Niveau de log valide
- Valeurs numériques positives
- Format des booléens

## Organisation des fichiers .env avec python-dotenv

Le système utilise `python-dotenv` pour une gestion robuste des fichiers de configuration :

### Hiérarchie des fichiers .env

```
.env.defaults  ← Valeurs par défaut (peut être versionné)
.env.local     ← Configuration locale (à ignorer dans git)
.env          ← Configuration générale (peut être versionné)
```

### Chargement automatique

Les fichiers sont chargés automatiquement dans cet ordre (chaque fichier surcharge le précédent) :

```python
# Chargement automatique au démarrage de password_utils
load_env_files()  # Charge .env.defaults → .env.local → .env
```

### Utilisation pratique

```bash
# Workflow de développement typique :
# 1. Copier env.example vers .env
cp env.example .env

# 2. Modifier vos vraies valeurs dans .env
echo "DEMO_API_EMAIL=votre.email@domain.com" >> .env
echo "DEMO_API_TOKEN=votre_token" >> .env

# 3. Créer .env.local pour des valeurs sensibles (ignoré par git)
echo "DEMO_API_PASSWORD=mot_de_passe_confidential" >> .env.local

# 4. Lancer l'application (charge automatiquement tous les fichiers)
python main.py
```

### Avantages de python-dotenv

- **✅ Chargement automatique** : Pas besoin de configuration manuelle
- **✅ Hiérarchie de configuration** : Fichiers par priorité
- **✅ Format standard** : Compatible avec tous les outils
- **✅ Sécurité** : Support des variables sensibles locales
- **✅ Développement** : Configuration flexible par environnement
