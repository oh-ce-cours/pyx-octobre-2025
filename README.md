# 📚 Projet PYx - Formation Python Avancé

> Repository pédagogique pour la formation Python avancé incluant exercices, corrections et démonstrations pratiques

## 🚀 À propos

Ce repository contient un ensemble complet de ressources pédagogiques pour l'enseignement du Python avancé, incluant des exercices pratiques, leurs corrections détaillées, des démonstrations interactives et une API de démonstration fonctionnelle.

## 📁 Structure du projet

### 📖 Documentation pédagogique
```
├── presentation.pdf          # Présentation principale du cours
├── handout.pdf              # Support de cours principal
├── sujets.pdf              # Sujets d'exercices
├── corrections.pdf         # Corrections des exercices
└── medias/                 # Ressources multimédia (logs, images, données)
```

### 🎯 Modules de formation

#### 🛠️ Administration système
**`corrections/administrationSysteme/`**
- **IP/** : Manipulation des adresses IP (conversion, validation, calculs de sous-réseaux)
- **manipulationFichiers/** : Exercices sur la gestion de fichiers (génération, organisation)
- **manipulationLogs/** : Analyse de logs Apache avec Python
- **manipulationTexte/** : Traitement de texte et extraction de données
- **scraping/** : Techniques de web scraping et collecte de données

#### 📊 Sciences des données
**`corrections/scipy/`**
- Scripts pandas pour manipulation de données
- Analyses scientifiques avec matplotlib/seaborn
- Simulations numériques (Lotka-Volterra, marches aléatoires)
- Traitement d'images et filtrage de signaux
- Nouvelles corrigées pour COVID-19

#### 🎮 Programmation orientée objet
**`corrections/poo/`** et **`pooAvancee/`**
- Concepts fondamentaux de l'OOP
- Design patterns et métaclasses
- Injection de dépendances
- Système d'événements personnalisés

#### 🔄 Programmation parallèle
**`corrections/parallelisme/`**
- Multiprocessing avec bibliothèque `multiprocessing`
- Concurrence asynchrone avec `asyncio`
- Threading et optimisations de performance
- Exemples pratiques de parallélisation

#### 🌐 Interfaces graphiques
**`corrections/gui/`**
- Applications Qt avec PyInstaller
- Tkinter pour interfaces simples
- Applications métier (calculatrice, tableur, paint)

#### 🔧 Intégration C/Python
**`corrections/integrationC/`**
- **ctypes/** : Interface avec bibliothèques C
- **cython/** : Optimisation de performance
- **embedPython/** : Intégration Python dans applications C

#### ✨ Fonctions avancées
**`corrections/fonctionsAvancees/`**
- Générateurs et décorateurs
- Pipelines de données fonctionnels
- Fonctions deprecated et migrations
- Patterns de programmation fonctionnelle

#### 📊 Dash et visualisation
**`corrections/dash/`**
- Applications Dash interactives
- Cross-filtering et dashboards
- Intégration matplotlib avec Plotly
- Application trading avec données en temps réel

#### 🗃️ Bases de données et modules
**`corrections/modules/`**
- Connexions SQLite et requêtes avancées
- Expressions régulières avancées
- Patterns de connexion et gestion d'erreurs

### 🔨 Autres cours spécialisés

#### 🎭 Ansible
**`autres_cours/ansible/`**
- Playbooks complets pour architectures 3-tiers
- Déploiement WordPress automatisé
- Gestion d'inventaires et rôles
- Exercices pratiques avec corrections

#### 🐍 Python avancé
**`autres_cours/python_avance/`**
- Présentations et handouts spécialisés
- Concepts avancés du langage Python

### 🚀 Démonstration API fonctionnelle

#### 🔥 **`tape_en_cours/demo_api/` - ⭐ MIS À JOUR ET FONCTIONNEL**

> **🎯 Disponible pour les élèves dès maintenant !**

Cette API de démonstration complète présente une interface CLI moderne pour la gestion d'utilisateurs et de machines virtuelles :

**Fonctionnalités principales :**
- **🔐 Authentification complète** : Création d'utilisateurs et tokens sécurisés
- **🖥️ Gestion de VMs** : Création, configuration et suivi de machines virtuelles
- **📊 Génération de rapports** : Formats JSON, Markdown et HTML
- **🎲 Données factices** : Génération automatique avec Faker
- **🔧 Interface CLI moderne** : Typer avec Rich pour une expérience utilisateur optimale

**Technologies utilisées :**
```python
# Dépendances principales
requests==2.32.5        # Client HTTP pour l'API
typer==0.19.2           # Interface CLI moderne
rich==13.9.4            # Terminal riche et coloré
faker==37.8.0           # Génération de données factices
python-dotenv>=1.0.0    # Gestion des variables d'environnement
```

**Commandes disponibles :**
```bash
# Créer un utilisateur
python main.py signup --name "Alice Dupont" --email "alice@exemple.com"

# Créer une VM
python main.py create --name "Ma VM" --ram 8 --disk 100

# Générer des données de test
python main.py generate --users 50 --max-vms 3

# Générer des rapports
python main.py report --type all --format html
```

**Configuration avancée :**
- Système de configuration hybride (.env files + variables d'environnement)
- Logging structuré avec `structlog`
- Gestion d'erreurs robuste avec retry automatique
- Authentification Bearer token sécurisée

## 🔄 GitHub Actions & Pages

### 🚀 Workflow de déploiement automatique

Le projet inclut une **GitHub Action** configurée dans `.github/workflows/docs.yml` qui :

1. **Se déclenche automatiquement** sur chaque push vers `main`
2. **Configuration Python 3.12** pour compatibilité maximale
3. **Installation des dépendances** depuis `tape_en_cours/demo_api/requirements.txt`
4. **Génération automatique de documentation** avec Sphinx/Pdoc3
5. **Déploiement sur GitHub Pages** pour accès facile aux étudiants

**🎯 Accès à la documentation :** [https://oh-ce-cours.github.io/pyx-octobre-2025](https://oh-ce-cours.github.io/pyx-octobre-2025)

### 📝 Outils de documentation inclus

Le workflow génère :
- **Documentation Sphinx** avec thème moderne Furo
- **Documentation Pdoc3** pour les modules Python
- **API Reference** automatique depuis les docstrings
- **Exemples de code** intégrés depuis les fichiers d'exemple

## 🛠️ Installation et utilisation

### Prérequis
- Python 3.12+
- pip (gestionnaire de paquets Python)

### Installation rapide

```bash
# Cloner le repository
git clone https://github.com/yourusername/pyx-octobre-2025.git
cd pyx-octobre-2025

# Pour demo_api (recommandé pour les élèves)
cd tape_en_cours/demo_api
pip install -r requirements.txt

# Test de l'installation
python main.py --help
python main.py version
```

### 🎓 Utilisation pédagogique

1. **📚 Explorez les exercices** dans les dossiers `corrections/`
2. **🔧 Testez demo_api** dans `tape_en_cours/demo_api/`
3. **📊 Consultez les rapports** générés automatiquement
4. **🎯 Suivez les sujets** dans `sujets.pdf`
5. **✅ Vérifiez vos solutions** avec `corrections.pdf`

## 📈 Statistiques du projet

- **📁 50+ modules d'exercices** organisés par thématique
- **🐍 100% Python moderne** (3.12+ features)
- **🔧 Code production-ready** avec gestion d'erreurs
- **📊 Documentation complète** générée automatiquement
- **🚀 GitHub Actions** pour déploiement continu

## 🔧 Déploiement GitHub Pages

### 🚀 Déploiement automatique (recommandé)
Le workflow GitHub Actions se déclenche automatiquement sur chaque push vers `main`.

### 📦 Déploiement manuel
Si vous préférez déployer manuellement :

```bash
# Depuis la racine du projet
./deploy_docs.sh

# Puis commiter et pousser
git add docs-deploy/
git commit -m "Deploy documentation"
git push origin main
```

### ⚙️ Configuration GitHub Pages
1. Allez dans **Settings** > **Pages** de votre repository
2. Sous **Source**, sélectionnez **GitHub Actions**
3. Sélectionnez le workflow **Deploy Documentation**
4. GitHub publiera automatiquement sur `https://oh-ce-cours.github.io/pyx-octobre-2025/`

## 🤝 Contribution

Ce repository pédagogique est conçu pour être :
- **🎯 Progressif** : Comprendre étape par étape
- **🔧 Pratique** : Code immédiatement utilisable
- **📚 Documenté** : Exemples clairs et commentés
- **🚀 Moderne** : Technologies Python actuelles

## 📞 Support

Pour toute question concernant les exercices ou l'API de démonstration, consultez :
1. La documentation générée automatiquement
2. Les fichiers `README.md` dans chaque module
3. Les commentaires détaillés dans le code source

---

*🔄 Dernière mise à jour : `tape_en_cours/demo_api` fonctionnel et prêt pour les étudiants !*
