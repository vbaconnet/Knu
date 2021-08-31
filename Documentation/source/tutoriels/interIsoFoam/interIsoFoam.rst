interIsoFoam
==============

Utilisez ces tutoriels de base pour découvrir ``isoAdvector``.

.. NOTE::

   Il suffit juste de réutiliser les tutoriels d'`interFoam<../interFoam/interFoam>`
   et de remplacer la ligne::

      application interFoam

   par::

      application interIsoFoam

   dans votre fichier ``system/controlDict``. Evidemment, 
   lorsque vous lancer une simulation, entrez la commande::

       $ interIsoFoam > log.interIsoFoam &

.. toctree::
   :maxdepth: 1

   houleReguliere
   houleIrreguliere
   mesurePressionOuvrage
   obstaclePoreux
   debitFranchissement
   batteurPiston
