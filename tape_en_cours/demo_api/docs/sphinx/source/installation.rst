Installation
============

Prérequis
---------

- Python 3.12.2 ou supérieur
- pip (gestionnaire de paquets Python)

Installation des dépendances
-----------------------------

1. Clonez le repository :

.. code-block:: bash

   git clone <repository-url>
   cd demo_api

2. Installez les dépendances :

.. code-block:: bash

   pip install -r requirements.txt

3. Configurez les variables d'environnement :

.. code-block:: bash

   cp env.example .env
   # Éditez le fichier .env avec vos paramètres

Installation en mode développement
----------------------------------

Pour installer le projet en mode développement :

.. code-block:: bash

   pip install -e .

Vérification de l'installation
-------------------------------

Testez l'installation en exécutant :

.. code-block:: bash

   python main.py --help
