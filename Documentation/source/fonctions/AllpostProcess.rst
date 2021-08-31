Gestion des scripts de post-traitement
=======================================

Informations
------------

* Nom du fichier : ``Knu/Scripts/Automatisation-OpenFOAM/AllpostProcess``

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
 
   $ AllpostProcess [OPTIONS] <script1> <script2> ... <scriptN>

**Options**

--log=<log_file>        définir un autre fichier log dans
                        lequel lire.
-h, --help              Afficher l'aide

.. WARNING::

    Si vous spécifiez un fichier log alternatif, mettez le bien en première
    option après ``AllpostProcess``, comme indiqué au dessus. Sinon,
    le traitement des scripts mis en paramètres ne sera pas bien effectué.

**Erreurs**

1 en cas de problème de lecture d'option
2 en cas de problème de lecture de fichier

Code source
------------

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Automatisation-OpenFOAM/AllpostProcess>`_
