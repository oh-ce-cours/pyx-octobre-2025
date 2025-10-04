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
