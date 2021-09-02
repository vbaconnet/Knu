.. outils documentation master file, created by
   sphinx-quickstart on Fri Apr 30 14:52:41 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Canal Numérique
===============

Bienvenue dans la documentation du canal numérique d'ACRI-IN. Vous y trouverez l'aide
pour la mise en place des tutoriels ainsi qu'un descriptif complet des scripts et programmes développés 
pour diverses applications. 

Installation
-------------

Ces outils font partie du package scripts-python-ACRI, téléchargeable avec la commande::

        git clone https://github.com/victor13165/Knu

Une fois téléchargé, allez dans le dossier et chargez les variables d'environnement::

	cd Knu
	source sourceMe

.. NOTE::

	Si vous souhaitez utiliser le solveur ``sedFoam`` vous devrez installer
	et compiler la dernière version vous-même (sauf si il est déjà installé).
	Le code source de ``sedFoam`` se télécharge à l'adresse::

		https://github.com/sedfoam/sedfoam

Tutoriels
---------

Des tutoriels détaillés pour tous types d'applications.

* **Solveurs**:
  :doc:`interFoam </tutoriels/interFoam/interFoam>` |
  :doc:`interIsoFoam </tutoriels/interIsoFoam/interIsoFoam>` |
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
  :doc:`Injection d'eau depuis une source mobile </tutoriels/overInterDyMFoam/faucetAndSink>` 

* **Sédimentation et transport de sédiments** :
  :doc:`Affouillement en 2D</tutoriels/sedFoam/2DPipelineScour>` |
  :doc:`Affouillement en 3D</tutoriels/sedFoam/3DScour>`

.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: Tutoriels

   tutoriels/interFoam/interFoam
   tutoriels/interIsoFoam/interIsoFoam
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
une courte présentation des théories utilisées pour la :doc:`génération de houle irrégulière<canal>`
du canal à houle d'ACRI-IN est fournie. Enfin des scripts d'automatisation pour OpenFOAM pour le 
:doc:`maillage<fonctions/Allmesh>`, le :doc:`lancement de calculs<fonctions/Allrun>`, 
la :doc:`gestion de scripts de post-traitement<fonctions/AllpostProcess>` et le 
:doc:`nettoyage<fonctions/Allclean>` de dossier est présenté.

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Documentation

   generationHoule
   postTraitement
   canal
   outils
   automatisation



Liens utiles 
-------------

* Introduction à OpenFOAM par `Joszef Nagy <https://www.youtube.com/watch?v=mGSUIXye9j4&list=PLcOe4WUSsMkH6DLHpsYyveaqjKxnEnQqB>`_

* **Modèles de turbulence modifiés pour interFoam** : `stabRAS <https://github.com/BjarkeEltardLarsen/stabRAS_v1712>`_ (version v1712) | 
  `kOmegaSSTBuoyancy <https://github.com/BrechtDevolder/buoyancyModifiedTurbulenceModels/tree/master/OFv1806>`_ (v1806)

* **Programmer avec OpenFOAM** : Ajout d'équation de `transport scalaire passif <https://www.youtube.com/watch?v=L94iYGvZr9Q>`_ |
  `Playlist complète <https://www.youtube.com/watch?v=_8A5CsIQ1xI&list=PLhPfNw4V4_YT9OgqS7ZPlot_Ucxzc6pQJ>`_ d'introduction à la 
  programmation en C++ | Un `cours <https://www.youtube.com/watch?v=KB9HhggUi_E>`_ de l'UCL de programmation pour OpenFOAM |
  `Plus de détails <https://www.youtube.com/watch?v=3iZfVmFkvB8>`_ sur OpenFOAM

.. NOTE::

  Des exemples de programmation avec OpenFOAM sont donnés dans les fichiers ``0.orig/Ua`` et ``0.orig/alpha_a``
  du tutoriel d':doc:`affouillement 2D </tutoriels/sedFoam/2DPipelineScour>`.
