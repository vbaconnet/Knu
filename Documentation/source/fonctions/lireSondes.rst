Exportation de mesures de sondes 
==================================

Informations
-------------


    * Fichier: ``Knu/Scripts/Post-traitement/lireSondes.py``
    * Auteur: Victor Baconnet
    * Date de dernière modification: 27 août 2021

Description
-------------

Lit les valeurs de chaque sonde et calcule la hauteur d'interface par interpolation
à la hauteur où :math:`\\alpha=0.5`, et écrit le signal calculé dans un fichier
au format ``.csv`` (peut être changé avec l'option ``--output <output>``).
                    
L'option ``--normalize`` vous permet de normaliser les valeurs d'interface à une
hauteur d'eau nulle. Cette normalisation se fait en prenant comme référence
la première valeur du signal, en considérant que cette valeur est la hauteur 
d'eau initiale.
                    
Entrées/sorties
----------------

* Lit les valeurs mesurées par les sondes dans les fichiers du dossier 
  ``postProcessing`` par défaut ``postProcessing/line``. Au lieu de ``line``,
  vous pouvez indiquer un autre nom avec l'option ``--linepath <name>``. Ce
  nom correspond au nom que vous avez donné à votre set de sondes dans 
  ``system/controlDict``.

* Ecrit les valeurs dans un fichier au format ``line_probes.csv`` par défaut
  mais peut être modifié avec l'option ``--outputfile <file>``.

Utilisation
----------------

.. code-block:: bash
    
    $ python3 lireSondes.py [OPTIONS]

--outputfile file       Fichier de sortie des mesures de sondes
--normalize fichier     Normaliser le signal avec une hauteur d'eau nulle
--linepath name         Nom du dossier où se trouvent les mesures des sondes.

Dépendances
----------------

* ``pandas``, ``scipy.interpolate``
* ``outilsLecture``, ``outilsDivers``
* ``sys``

Code source
----------------

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Post-traitement/lireSondes.py>`_
