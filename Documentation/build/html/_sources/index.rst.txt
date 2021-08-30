.. outils documentation master file, created by
   sphinx-quickstart on Fri Apr 30 14:52:41 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Canal Numérique
===============

Bienvenue dans la documentation du canal numérique d'ACRI-IN. Vous y trouverez l'aide
pour la mise en place des tutoriels, un descriptif complet des scripts et programmes, le guide de programmation de la routine de génération de houle du canal, ainsi qu'un guide de résolution de problèmes.

Installation
-------------

Ces outils font partie du package scripts-python-ACRI, téléchargeable avec la commande::

        git clone https://github.com/victor13165/Knu

Tutoriels
---------

Des tutoriels détaillés pour tous types d'applications.

* **Solveurs**:
  :doc:`interFoam </tutoriels/interFoam/interFoam>` |
  :doc:`olaFlow </tutoriels/olaFlow/olaFlow>` |
  :doc:`overInterDyMFoam </tutoriels/overInterDyMFoam/overInterDyMFoam>` |
  :doc:`sedFoam </tutoriels/sedFoam/sedFoam>`

* **Génération de houle**:
  :doc:`Régulière </tutoriels/interFoam/houleReguliere>`   |
  :doc:`Irrégulière </tutoriels/interFoam/houleIrreguliere>` |
  :doc:`Batteur piston </tutoriels/interFoam/batteurPiston>`

* **Mesures sur des ouvrages**: 
  :doc:`Débit de franchissement </tutoriels/interFoam/debitFranchissement>` |
  :doc:`Pression </tutoriels/interFoam/mesurePressionOuvrage>`

* **Ecoulements en milieux poreux** :
  :doc:`Darcy-Fochheimer </tutoriels/interFoam/obstaclePoreux>` |
  :doc:`VARANS </tutoriels/olaFlow/obstaclePoreux>`

* **Maillages dynamiques** :
  :doc:`Batteur piston </tutoriels/interFoam/batteurPiston>`  |
  :doc:`Digue flottante de Monaco </tutoriels/overInterDyMFoam/digueMonaco>` |
  :doc:`Objet Flottant </tutoriels/overInterDyMFoam/objetFlottant>` |
  :doc:`Injection d'eau depuis une source mobile </tutoriels/overInterDyMFoam/faucetAndSink>` 

.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: Tutoriels

   tutoriels/interFoam/interFoam
   tutoriels/olaFlow/olaFlow
   tutoriels/overInterDyMFoam/overInterDyMFoam
   tutoriels/sedFoam/sedFoam


Documentation des programmes
-----------------------------

Une documentation exhaustive des programmes et librairies développées
pour la :doc:`génération de houle<generationHoule>`, le 
:doc:`post-traitement<postTraitement>` de données, et quelques :doc:`librairies<outils>`
construites pour l'aide à la :doc:`lecture de paramètres<fonctions/outilsLecture>` et 
:doc:`l'exportation<fonctions/outilsExcel>` de données vers des fichiers Excel. En complément,
une courte présentation des théories utilisées pour la :doc:`génération de houle
 irrégulière<canal>` du canal à houle d'ACRI-IN est fournie.

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Documentation

   generationHoule
   postTraitement
   canal
   outils
