Modules API
===========

Cette section contient la documentation automatique de tous les modules Python du projet Demo API.

.. note::
   Cette documentation est générée automatiquement à partir du code source.
   Pour régénérer la documentation, exécutez le script ``generate_modules.py``.

Modules principaux
------------------

.. toctree::
   :maxdepth: 4

   main
   report_manager
   vm_manager

Modules utilitaires
-------------------

.. toctree::
   :maxdepth: 4

   utils/index

Modules de rapports
-------------------

.. toctree::
   :maxdepth: 4

   reports/index

Modules de services
--------------------

.. toctree::
   :maxdepth: 4

   services/index

Auto-découverte
---------------

Pour découvrir automatiquement tous les modules du projet, utilisez :

.. code-block:: bash

   python docs/sphinx/source/generate_modules.py

Cette commande générera automatiquement tous les fichiers de documentation
pour les modules Python trouvés dans le projet.
