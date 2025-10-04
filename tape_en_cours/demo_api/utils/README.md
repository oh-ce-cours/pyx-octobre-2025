# Guide d'utilisation sécurisée des mots de passe

## Variables d'environnement

Le système de gestion des mots de passe utilise les variables d'environnement suivantes :

### Variables disponibles

- `DEMO_API_EMAIL` : Email pour se connecter à l'API
- `DEMO_API_PASSWORD` : Mot de passe pour se connecter à l'API

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
