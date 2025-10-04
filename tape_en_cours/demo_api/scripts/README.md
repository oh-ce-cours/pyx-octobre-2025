# Scripts Utilitaires

Ce dossier contient tous les scripts utilitaires pour la démo API.

## Scripts Disponibles

### 🎲 `generate_data.py`
Générateur de données factices avec Faker pour créer des utilisateurs et VMs réalistes.

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

### 🚀 `create_data_via_api.py` ✨ **AMÉLIORÉ AVEC RICH**
Créateur de données via l'API en utilisant le générateur Faker avec un affichage Rich modernisé.

**Nouvelles fonctionnalités Rich :**
- 🎨 Panneaux colorés et encadrés pour les sections
- 📊 Tableaux structurés pour la configuration et statistiques  
- ⏳ Barres de progression en temps réel avec spinner
- 🎯 Messages contextuels colorés (succès/erreur)
- 🔄 Séparation claire entre logique métier et représentation

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

### 🧹 `quick_cleanup.py`
Script de nettoyage pour supprimer toutes les VMs et utilisateurs.

**Commandes disponibles :**
- `cleanup` : Nettoie les données (simulation par défaut)

**Exemples d'usage :**
```bash
# Mode simulation (par défaut)
python scripts/quick_cleanup.py cleanup

# Suppression réelle
python scripts/quick_cleanup.py cleanup --real

# Avec délai personnalisé
python scripts/quick_cleanup.py cleanup --real --delay 3
```

## Configuration

Tous les scripts utilisent la configuration définie dans `utils/config.py` pour :
- URL de l'API
- Identifiants d'authentification
- Paramètres de connexion

## Scripts de Démonstration

### 🎭 `demo_rich_improvements.py`
Démonstration des améliorations Rich dans `create_data_via_api.py`. Montre la différence entre l'ancien style (typer.echo) et le nouveau style (Rich) sans nécessiter une connexion API.

```bash
# Voir la démonstration des améliorations
python scripts/demo_rich_improvements.py
```

### 🧪 `test_rich_display.py`
Script de test pour valider les fonctionnalités Rich utilisées dans le script principal.

## Prérequis

- Python 3.8+
- Dépendances installées (`pip install -r requirements.txt`)
  - `rich` pour l'affichage amélioré
  - `typer` pour l'interface CLI
- API démarrée et accessible (pour les scripts de création de données)

## Notes Importantes

⚠️ **Attention** : Le script `quick_cleanup.py` peut supprimer définitivement toutes les données. Utilisez toujours le mode simulation (`--real` non spécifié) pour tester d'abord.

💡 **Conseil** : Utilisez `generate_data.py` pour créer des données de test, puis `create_data_via_api.py` pour les insérer dans l'API.

🎨 **Rich** : Le script `create_data_via_api.py` utilise maintenant Rich pour un affichage moderne avec couleurs, tableaux et barres de progression.
