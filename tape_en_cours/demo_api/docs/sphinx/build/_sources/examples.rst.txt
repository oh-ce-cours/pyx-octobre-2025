Exemples d'utilisation
=====================

Cette section contient des exemples pratiques d'utilisation de Demo API.

Génération de données de test
-----------------------------

Créer des utilisateurs et des VMs de test :

.. code-block:: bash

   # Générer 10 utilisateurs et 5 VMs
   python main.py generate-data --count 10 --vm-count 5
   
   # Générer avec des données spécifiques
   python main.py generate-data --count 20 --vm-count 10 --os ubuntu-20.04

Gestion des VMs
----------------

Créer et gérer des machines virtuelles :

.. code-block:: bash

   # Créer une VM simple
   python main.py create-vm --name "Serveur-Web" --os "ubuntu-20.04"
   
   # Créer une VM avec des spécifications
   python main.py create-vm --name "DB-Server" --os "centos-8" --ram 8 --cpu 4

Génération de rapports
-----------------------

Créer des rapports dans différents formats :

.. code-block:: bash

   # Rapport complet en tous formats
   python main.py report --type all --format all
   
   # Rapport HTML uniquement
   python main.py report --type users-vms --format html
   
   # Rapport JSON pour intégration
   python main.py report --type status --format json

Nettoyage et maintenance
-------------------------

Gérer les données de test :

.. code-block:: bash

   # Nettoyage complet (avec confirmation)
   python main.py cleanup --confirm
   
   # Nettoyage des VMs uniquement
   python main.py cleanup --vm-only --confirm
