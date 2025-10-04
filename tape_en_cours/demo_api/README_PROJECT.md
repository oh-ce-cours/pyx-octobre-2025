# Demo API - Projet Documentation

## 📍 Architecture du projet

Ce projet fait partie d'une structure Git plus large. Voici l'organisation :

```
pyx-octobre-2025/
├── .github/workflows/          # Actions GitHub (racine Git)
├── tape_en_cours/
│   └── demo_api/               # Ce projet Python
│       ├── scripts/            # Scripts utilitaire
│       ├── docs/               # Documentation (Sphinx + pdoc3)
│       ├── utils/              # Modules Python
│       └── main.py             # Point d'entrée
└── autres_projets/             # Autres exercices du cours
```

## 🚀 GitHub Actions

Les workflows GitHub Actions sont dans `.github/workflows/` à la **racine du depot Git**, mais :
- Le `working-directory` pointe vers `tape_en_cours/demo_api/`
- Les chemins sont relatifs à la racine Git

## 📚 Documentation disponible

Après chaque push sur `main` :

- **Sphinx (Furo)** : https://votrenom.github.io/repo/
- **pdoc3** : https://votrenom.github.io/repo/ (en changeant le `publish_dir`)

## 🔧 Commandes utiles

```bash
# Depuis la racine du projet (tape_en_cours/demo_api/)
python scripts/generate_docs.py

# Déployement manuel
python scripts/deploy_docs.py

# Vérifier la racine Git
git rev-parse --show-toplevel
```
