Automatisation de lancement de calculs
======================================

Informations
------------

* Nom du fichier : ``Knu/Scripts/Automatisation-OpenFOAM/Allrun``

* Auteur: Victor Baconnet
    
* Date de dernière modification: 08 Juillet 2021

Description
------------

Lance le calcul OpenFOAM selon le solveur défini dans controlDict
Peut lancer le calcul en parallèle selon les critères définis dans
decomposeParDict. Permet aussi de lancer ``setFields``, 
``surfaceFeatureExtract`` et ``topoSet``.

.. NOTE::

    Il est conseillé de faire en sorte que ce fichier soit accessible dans la
    variable d'environnement ``$PATH``. Pour cela, dans le dossier Knu, lancez::

        $ source sourceMe


Utilisation
------------

.. code-block:: bash
 
   $ Allrun [OPTIONS]


-c, --clean             Nettoyer le répertoire (maillage, dossiers de résultats,
                        dossiers de processeurs, fichiers log)
-s, --setfields         Lancer setFields selon les critères de 
                        setFieldsDict
-e, --surfacefeature    Lancer surfaceFeatureExtract
-t, --toposet           Lancer topoSet selon les critères de topoSetDict
-p, --parallel          Lancer le calcul en parallèle avec le nombre de 
                        processeurs défini dans decomposeParDict
-r, --noreconstruct     Pour ne pas reconstruire les fichiers après 
                        le calcul parallèle
-n, --nosolve           Ne pas lancer le solveur. Si -p ou -r sont activées,
                        elles ne seront pas prises en compte et généreront un warning
-h, --help              Afficher l'aide


**Erreurs**


* 1 pour argument ou option invalide
* 4 si erreur dans decomposePar
* 7 si erreur de lancement du solveur
* 8 si erreur dans reconstructPar 
* 9 si erreur dans la copie du dossier 0
* 10 si erreur dans setFields
* 11 si erreur dans topoSet
* 12 si erreur dans surfaceFeatureExtract

Code source
------------

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Automatisation-OpenFOAM/Allrun>`_