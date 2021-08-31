Mesure de débit de franchissement
==================================

Il vous suffit de reprendre le :doc:`tutoriel de houle régulière<../interFoam/debitFranchissement>`, en
remplaçant la ligne::

    application     interFoam;

par la ligne::

    application     interIsoFoam;

dans le fichier ``system/controlDict``.