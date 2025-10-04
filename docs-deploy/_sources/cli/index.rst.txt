Interface en ligne de commande
=============================

Documentation de l'interface CLI de Demo API.

Commandes principales
--------------------

.. code-block:: bash

   # Génération de données de test
   python main.py generate-data --count 10
   
   # Création d'une VM
   python main.py create-vm --name "VM-Test" --os "ubuntu-20.04"
   
   # Génération de rapports
   python main.py report --type all --format all
   
   # Nettoyage des données
   python main.py cleanup --confirm

Options communes
----------------

- ``--verbose`` ou ``-v`` : Mode verbeux
- ``--help`` : Aide pour une commande spécifique
- ``--output-dir`` ou ``-o`` : Répertoire de sortie personnalisé

Exemples d'utilisation
-----------------------

Voir la section :doc:`quickstart` pour des exemples détaillés.
