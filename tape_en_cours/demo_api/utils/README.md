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

## Variables d'environnement

Le système de gestion des mots de passe utilise les variables d'environnement suivantes :

### Variables disponibles

- `DEMO_API_EMAIL` : Email pour se connecter à l'API
- `DEMO_API_PASSWORD` : Mot de passe pour se connecter à l'API
- `DEMO_API_TOKEN` : Token d'authentification (optionnel - créé automatiquement)
- `DEMO_API_DEBUG` : Active le mode debug (true/false)
- `DEMO_API_LOG_LEVEL` : Niveau de logging (DEBUG, INFO, WARNING, ERROR)

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

#### **Fichier .env :**
- `save_token_to_env_file()` : Sauvegarde un token dans un fichier .env
- `load_token_from_env_file()` : Charge un token depuis un fichier .env

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
