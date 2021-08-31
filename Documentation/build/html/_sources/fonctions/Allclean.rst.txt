Nettoyer un répertoire OpenFOAM
===============================

Informations
------------

* Nom du fichier : ``Knu/Scripts/Automatisation-OpenFOAM/Allclean``

* Auteur: Victor Baconnet
    
* Date de dernière modification: 08 Juillet 2021

Description
------------

Lance une série de scripts lorsque la simulation est terminée. La
fin de la simulation est basée sur le fichier log de sortie de 
simulation, au format ``log.nomSolver``, où ``nomSolver`` est le nom du 
solveur donné dans ``controlDict``. Il est possible de changer le nom
du fichier avec l'option ``--log=<fichier_log>``.

.. NOTE::

    Il est conseillé de faire en sorte que ce fichier soit accessible dans la
    variable d'environnement ``$PATH``. Pour cela, dans le dossier Knu, lancez::

        $ source sourceMe


Utilisation
------------

.. code-block:: bash
 
   $ Allclean [OPTIONS]
	
Permet de nettoyer un répertoire OpenFOAM. Nettoie uniquement les 
fichiers log, le maillage, les dossiers temporels et les dossiers
processeurs.

**Options**

-n, --notmesh       Ne pas effacer le maillage
-h, --help          Afficher l'aide


Code source
------------

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Automatisation-OpenFOAM/Allclean>`_
