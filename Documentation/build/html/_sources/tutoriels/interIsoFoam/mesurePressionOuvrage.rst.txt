Mesure de pression sur un ouvrage
==================================

Il vous suffit de reprendre le :doc:`tutoriel de mesure de pression <../interFoam/mesurePressionOuvrage>`, en
remplaçant la ligne::

    application     interFoam;

par la ligne::

    application     interIsoFoam;

dans le fichier ``system/controlDict``.
