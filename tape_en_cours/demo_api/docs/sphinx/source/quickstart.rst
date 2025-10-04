Guide de démarrage rapide
=========================

Ce guide vous permettra de commencer rapidement avec Demo API.

Configuration initiale
----------------------

1. **Configuration de l'environnement** :

   Créez un fichier `.env` basé sur `env.example` :

   .. code-block:: bash

      cp env.example .env

2. **Configuration des variables** :

   Éditez le fichier `.env` avec vos paramètres :

   .. code-block:: text

      API_BASE_URL=http://localhost:8000
      API_USERNAME=admin
      API_PASSWORD=password
      LOG_LEVEL=INFO

Premiers pas
------------

**Génération de données de test** :

.. code-block:: bash

   python main.py generate-data --count 10

**Création d'une VM** :

.. code-block:: bash

   python main.py create-vm --name "VM-Test" --os "ubuntu-20.04"

**Génération de rapports** :

.. code-block:: bash

   python main.py report --type all --format all

**Nettoyage des données** :

.. code-block:: bash

   python main.py cleanup --confirm

Commandes utiles
----------------

- ``python main.py --help`` : Affiche l'aide générale
- ``python main.py <command> --help`` : Aide pour une commande spécifique
- ``python main.py report --verbose`` : Mode verbeux pour les rapports
