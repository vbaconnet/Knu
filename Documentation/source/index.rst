.. outils documentation master file, created by
   sphinx-quickstart on Fri Apr 30 14:52:41 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Canal Numérique
===============

Bienvenue dans la documentation du canal numérique d'ACRI-IN. Vous y trouverez l'aide
pour la mise en place des tutoriels, un descriptif complet des scripts et programmes, le guide de programmation de la routine de génération de houle du canal, ainsi qu'un guide de résolution de problèmes.

Installation
============

Ces outils font partie du package scripts-python-ACRI, téléchargeable avec la commande::

        git clone https://github.com/victor13165/Knu

***********
Tutoriels
***********

Des tutoriels détaillés pour tous types d'applications:

* Houle :doc:`régulière </tutoriels/interFoam/houleReguliere>` et :doc:`régulière </tutoriels/interFoam/houleIrreguliere>`
* Mesure de débit de franchissement : `Port-La-Galère`
* Mesure de pression sur un `ouvrage`
* Ecoulements en milieux poreux: `interFoam` et `olaFlow`

.. toctree::
   :maxdepth: 3
   :hidden:
   :caption: Tutoriels

   tutoriels


Index
======

.. toctree::
   :maxdepth: 2
   
   tutoriels
   canal
   modules

