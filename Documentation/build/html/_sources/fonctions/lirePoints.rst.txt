Exportation de mesures de points 
=================================

Informations
-------------

    * Fichier : ``Knu/Scripts/Post-traitement/lireSondes.py``
    * Auteur: Victor Baconnet
    * Date de dernière modification: 27 août 2021

Description
-------------

Lit les valeurs de mesures de pression dans les fichiers du dossier ``postProcessing``.
Par défaut, la recherche se fait dans le dossier ``postProcessing/points``. Vous
pouvez modifier la destination ``points`` avec la commande ``--name name``. Ce 
dossier porte le même nom que celui que vous avez donné à votre set de points
dans ``system/controlDict``. 

Une fois dans le dossier ``postProcessing/points``, le programme prendre par 
défaut le premier fichier et en extraira le nom du cloud correspondant. Si il n'y
a pas de fichiers cloud disponibles, renverra une erreur. Si il y a plusieurs
fichiers clouds disponibles, le programme renverra une erreur en vous affichant
tous les clouds disponibles.

Un cloud est considéré comme valide si son nom de fichier est du type
``<nom>_<champ>.xy``. ``champ`` est par défaut ``p`` pour lire des mesures de 
pression, mais peut être changé avec l'option ``--champ <champ>``.
                    
Entrées/sorties
---------------

* Lit les valeurs mesurées par les sondes dans les fichiers du dossier 
  ``postProcessing`` par défaut ``postProcessing/line``. Au lieu de ``line``,
  vous pouvez indiquer un autre nom avec l'option ``--linepath <name>``. Ce
  nom correspond au nom que vous avez donné à votre set de sondes dans 
  ``system/controlDict``.

* Ecrit les valeurs dans un fichier au format ``line_probes.csv`` par défaut
  mais peut être modifié avec l'option ``--outputfile <file>``.

Utilisation
-------------

--outputfile file       Fichier de sortie des mesures de sondes
--name name             Nom du dossier où se trouvent les mesures. Ce nom correspond
                        au chemin ``postProcessing/<name>``.
--champ champ           Champ de données à lire. Exemple de champs: 
                        ``alpha.water``, ``p``, ``U``...
--cloudname cloud       Nom du cloud de points. Ce nom du cloud correspond au
                        nom de fichier de type ``<cloud>_<champ>.xy``

Dépendances
-------------

* ``pandas``
* ``outilsLecture``, ``outilsDivers``
* ``sys``, ``os`` 

Code source
-------------

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Post-traitement/lirePoints.py>`_
