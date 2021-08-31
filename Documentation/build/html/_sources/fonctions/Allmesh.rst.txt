Automatisation de maillage
===========================

Informations
------------

* Nom du fichier : ``Knu/Scripts/Automatisation-OpenFOAM/Allmesh``

* Auteur: Victor Baconnet
    
* Date de dernière modification: 08 Juillet 2021

Description
------------

Outil d'automatisation de maillage (blockMesh, snappyHexMesh), avec possibilité de
lancement en parallèle et gestion des erreurs. Par défaut, ne lance que blockMesh.
Pour lancer snappyHexMesh, utilisez l'option -S ou --snappyhexmesh. 
Le script supprime le maillage existant par défaut. blockMesh n'est jamais lancé en parallèle.

.. NOTE::

    Il est conseillé de faire en sorte que ce fichier soit accessible dans la
    variable d'environnement ``$PATH``. Pour cela, dans le dossier Knu, lancez::

        $ source sourceMe


Utilisation
------------

.. code-block:: bash
 
   $ Allmesh [OPTIONS]


**Options**

-c, --clean             Nettoyer le répertoire. Le maillage existant
                        (polyMesh) est supprimé par défaut.
-p, -parallel           Lancer snappyHexMesh en parallèle avec le nombre de
                        processeurs défini dans decomposeParDict.
-e, --extrudemesh       Lancer l'extrusion de maillage selon les 
                        critères définis dans extrudeMeshDict.
-S, --snappyhexmesh     Lancer snappyHexMesh selon les critères 
                        définis dans snappyHexMeshDict.
-h, --help              Afficher l'aide

**Erreurs**

* 1 pour argument ou option invalide"
* 2 si erreur dans blockMesh"
* 3 si erreur dans snappyHexMesh"
* 4 si erreur dans decomposePar"
* 5 si erreur dans extrudeMesh"
* 6 si erreur dans reconstructParMesh"

Dépendances
------------

* ``numpy``
* ``sys``, ``os``
* ``outilsLecture`` 

Code source
------------

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Automatisation-OpenFOAM/Allmesh>`_
