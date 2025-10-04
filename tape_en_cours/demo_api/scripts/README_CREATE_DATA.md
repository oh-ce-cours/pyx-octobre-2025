# 🚀 Créateur de données via API avec Faker

Ce script permet de créer des données réalistes via l'API en utilisant le générateur Faker intégré au projet.

## 📋 Fonctionnalités

- **Création d'utilisateurs** : Génère des utilisateurs français réalistes avec Faker
- **Création de VMs** : Génère des machines virtuelles avec des configurations réalistes
- **Dataset complet** : Crée un ensemble complet d'utilisateurs et de VMs
- **Gestion des lots** : Traite les données par lots pour éviter de surcharger l'API
- **Authentification** : Support de l'authentification API avec gestion des erreurs
- **Statistiques** : Affiche des statistiques détaillées sur les données créées

## 🛠️ Installation et Configuration

### Prérequis

1. **API en fonctionnement** : Assurez-vous que votre API demo_api est démarrée
2. **Configuration** : Configurez les identifiants dans `utils/config.py` ou utilisez les paramètres en ligne de commande

### Configuration des identifiants

Vous pouvez configurer les identifiants de plusieurs façons :

1. **Via la configuration** (recommandé) :
   ```python
   # Dans utils/config.py
   DEMO_API_EMAIL = "votre_email@example.com"
   DEMO_API_PASSWORD = "votre_mot_de_passe"
   ```

2. **Via les paramètres en ligne de commande** :
   ```bash
   python create_data_via_api.py users --email admin@example.com --password secret
   ```

## 🎯 Utilisation

### Commandes disponibles

#### 1. Créer des utilisateurs

```bash
# Créer 10 utilisateurs avec les paramètres par défaut
python create_data_via_api.py users

# Créer 20 utilisateurs avec des lots de 5
python create_data_via_api.py users --count 20 --batch-size 5

# Créer des utilisateurs avec authentification personnalisée
python create_data_via_api.py users --email admin@example.com --password secret
```

#### 2. Créer des VMs

```bash
# Créer 20 VMs avec les paramètres par défaut
python create_data_via_api.py vms

# Créer 50 VMs avec des lots de 10
python create_data_via_api.py vms --count 50 --batch-size 10

# Créer des VMs avec délai entre les lots
python create_data_via_api.py vms --delay 1.0
```

#### 3. Créer un dataset complet

```bash
# Créer 20 utilisateurs + 50 VMs
python create_data_via_api.py full-dataset --users 20 --vms 50

# Créer un dataset et le sauvegarder
python create_data_via_api.py full-dataset --users 30 --vms 100 --output mon_dataset.json

# Créer un dataset avec mode verbeux
python create_data_via_api.py full-dataset --users 10 --vms 25 --verbose
```

#### 4. Vérifier le statut

```bash
# Afficher le statut actuel de l'API
python create_data_via_api.py status

# Statut avec authentification personnalisée
python create_data_via_api.py status --email admin@example.com --password secret
```

### Paramètres communs

- `--count, -c` : Nombre d'éléments à créer (utilisateurs ou VMs)
- `--batch-size, -b` : Taille des lots (défaut: 5)
- `--delay, -d` : Délai entre les lots en secondes (défaut: 0.5)
- `--email, -e` : Email pour l'authentification API
- `--password, -p` : Mot de passe pour l'authentification API
- `--verbose, -v` : Mode verbeux avec détails supplémentaires
- `--output, -o` : Fichier de sortie pour sauvegarder les données

## 📊 Exemples d'utilisation

### Scénario 1 : Peuplement initial

```bash
# Créer un dataset initial de 50 utilisateurs et 100 VMs
python create_data_via_api.py full-dataset --users 50 --vms 100 --output dataset_initial.json
```

### Scénario 2 : Ajout progressif

```bash
# Ajouter 10 nouveaux utilisateurs
python create_data_via_api.py users --count 10

# Ajouter 25 nouvelles VMs
python create_data_via_api.py vms --count 25
```

### Scénario 3 : Test avec petits volumes

```bash
# Test rapide avec 5 utilisateurs et 10 VMs
python create_data_via_api.py full-dataset --users 5 --vms 10 --verbose
```

## 🔧 Personnalisation

### Ajuster les délais

Pour éviter de surcharger l'API, vous pouvez ajuster les délais :

```bash
# Délai plus long entre les lots
python create_data_via_api.py users --delay 2.0

# Lots plus petits avec délai plus court
python create_data_via_api.py vms --batch-size 3 --delay 0.2
```

### Mode verbeux

Le mode verbeux affiche des détails supplémentaires :

```bash
python create_data_via_api.py full-dataset --users 10 --vms 20 --verbose
```

## 🚨 Gestion des erreurs

Le script gère automatiquement :

- **Erreurs d'authentification** : Messages clairs si l'authentification échoue
- **Erreurs de connexion** : Gestion des problèmes de réseau
- **Erreurs de validation** : Validation des données avant envoi
- **Erreurs partielles** : Continue même si certaines créations échouent

### Messages d'erreur courants

1. **"Impossible de s'authentifier avec l'API"**
   - Vérifiez que l'API est démarrée
   - Vérifiez les identifiants dans la config ou utilisez --email et --password

2. **"Aucun utilisateur trouvé dans l'API"**
   - Créez d'abord des utilisateurs avec la commande `users`

3. **"Erreur lors de la création"**
   - Vérifiez les logs pour plus de détails
   - Réduisez la taille des lots ou augmentez le délai

## 📈 Statistiques

Le script affiche des statistiques détaillées :

- Nombre d'éléments créés
- Taux de succès
- Répartition par utilisateur (pour les VMs)
- Aperçu des données créées (en mode verbeux)

## 🧪 Tests

Pour tester le script avant utilisation :

```bash
# Tester les générateurs de données
python test_create_data.py

# Tester avec un petit dataset
python create_data_via_api.py full-dataset --users 2 --vms 3 --verbose
```

## 💡 Conseils d'utilisation

1. **Commencez petit** : Testez d'abord avec de petits volumes
2. **Utilisez les délais** : Ajustez les délais selon la performance de votre API
3. **Surveillez les logs** : Activez le mode verbeux pour le débogage
4. **Sauvegardez** : Utilisez --output pour sauvegarder les données créées
5. **Vérifiez le statut** : Utilisez la commande `status` pour vérifier l'état

## 🔗 Intégration

Ce script s'intègre parfaitement avec :

- **generate_data.py** : Pour la génération de données statiques
- **main.py** : Pour les autres fonctionnalités du projet
- **report_manager.py** : Pour générer des rapports sur les données créées

## 📝 Logs

Les logs sont automatiquement générés via le système de logging du projet. Consultez les logs pour :

- Détails des opérations
- Erreurs et exceptions
- Statistiques de performance
- Informations de débogage
