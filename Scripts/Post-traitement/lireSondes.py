#!/usr/bin/env python3

"""
Informations
============

    * Fichier : ``Knu/Post-traitement/lireSondes.py``
    * Auteur: Victor Baconnet
    * Date de dernière modification: 27 août 2021

Description
============

Lit les valeurs de chaque sonde et calcule la hauteur d'interface par interpolation
à la hauteur où :math:`\\alpha=0.5`, et écrit le signal calculé dans un fichier
au format ``.csv`` (peut être changé avec l'option ``--output <output>``).
                    
L'option ``--normalize`` vous permet de normaliser les valeurs d'interface à une
hauteur d'eau nulle. Cette normalisation se fait en prenant comme référence
la première valeur du signal, en considérant que cette valeur est la hauteur 
d'eau initiale.
                    
Entrées/sorties
===============

* Lit les valeurs mesurées par les sondes dans les fichiers du dossier 
  ``postProcessing`` par défaut ``postProcessing/line``. Au lieu de ``line``,
  vous pouvez indiquer un autre nom avec l'option ``--linepath <name>``. Ce
  nom correspond au nom que vous avez donné à votre set de sondes dans 
  ``system/controlDict``.

* Ecrit les valeurs dans un fichier au format ``line_probes.csv`` par défaut
  mais peut être modifié avec l'option ``--outputfile <file>``.

Utilisation
===========

  $ python3 lireSondes.py [OPTIONS]

--outputfile file       Fichier de sortie des mesures de sondes
--normalize fichier     Normaliser le signal avec une hauteur d'eau nulle
--linepath name         Nom du dossier où se trouvent les mesures des sondes.

Dépendances
============

* ``pandas``, ``scipy.interpolate``
* ``outilsLecture``, ``outilsDivers``
* ``sys``

Code source
============

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Post-traitement/lireSondes.py>`_
"""

import os
import pandas as pd
import scipy.interpolate
import outilsLecture as olec
import outilsDivers as odiv
import sys

if __name__ == "__main__":

    #==========================================================================
    #------------------- Lecture des options ----------------------------------
    #==========================================================================

    #Read output file option
    outputFile = olec.readFileOption(sys.argv, ["-output","--output",
                                                "-outputfile","--outputfile"],
                                    default = "line_probes.csv",
                                    extension = "csv")

    # normalisation des résultats pour avoir un signal centré en y=0
    normalize = olec.readOption(sys.argv, ["-normalize", "--normalize"])
    
    # Chemin vers les valeurs de sondes
    linePath = olec.readDirOption(sys.argv, ["--linepath","-linepath"],
                                  default = "line")

    #==========================================================================
    #------------------- Initialisation et intervalle de temps ----------------
    #==========================================================================

    # Dossier postProcessing
    cwd = 'postProcessing/'+linePath

    # Vérification qu'il n'est pas vide
    if os.listdir(cwd) != []:
        print("Lecture des fichiers dans {}".format(cwd))
        all_folders = os.listdir(cwd) # Stocker tous les temps dans un tableau
    else:
        raise ValueError('{} est vide!'.format(cwd))

    # Création du vecteur temporel
    print("Création du vecteur temporel")
    time_vec = sorted([float(i) for i in all_folders]) # Trier tous les temps

    # Lecture des temps min et max à lire
    tmin = olec.readValueOption(sys.argv, ['-tmin', '--tmin'], default = time_vec[0])
    tmax = olec.readValueOption(sys.argv, ['-tmax', '--tmax'], default = time_vec[-1])
    print("Intervalle de temps : [{},{}]".format(tmin,tmax))

    # Trouver les index des temps demandés dans le tableau des temps time_vec
    tminIndex = odiv.find(time_vec, tmin, default = 0)    # Si pas trouvé, 0
    tmaxIndex = odiv.find(time_vec, tmax, default = None) # Si pas trouvé, None
    print("index [{},{}]".format(tminIndex,tmaxIndex))
    time_vec = time_vec[tminIndex:tmaxIndex] # Récupérer les temps demandés

    # Faire la même chose avec les noms des dossiers stockés dans all_folders
    for idx, time in enumerate(time_vec):
        if str(time).split(".")[-1] == "0":  # si on tombe sur 15.0, garder 15
            all_folders[idx] = str(time).split(".")[0]
        else:
            all_folders[idx] = str(time)

    # Ne garder que les fichiers dont on a besoin
    all_folders = all_folders[tminIndex:tmaxIndex] 
    total_time_steps = len(time_vec)

    #==========================================================================
    #-------------------------- Traitement des sondes ------------------------
    #==========================================================================

    # Récupérer le nom des sondes
    lines = []
    for filename in os.listdir(os.path.join(cwd, all_folders[0])):
        if filename.endswith('alpha.water.xy'):
            lines.append(filename.split('_')[0])
            print("Sonde trouvée :",filename.split('_')[0])
    if lines == []:
        raise ValueError('Aucun fichier au format *alpha_water.xy trouvé')

    # initialisation du dataframe qui va stocker toutes les valeurs
    df = pd.DataFrame(index=time_vec, columns=lines)

    # Trier le dataframe pour avoir le nom des sondes dans l'ordre
    # au cas où elles seraient numérotées
    df.sort_index(axis=1, inplace = True)  

    # Extraction de l'interface à partir de chaque fichier
    print("Extraction du champ alpha.water mesuré par chaque sonde...")

    # Parcourir chaque dossier temporel
    for br, folder in enumerate(all_folders, 1):  
        
        print('time step: {} s, ({}/{})'.format(folder, br, total_time_steps))
        folder_path = os.path.join(cwd, folder)
        
        # Parcourir chaque fichier sonde dans le dossier temporel
        for filename in os.listdir(folder_path):

            probename = filename.split('_')[0]
            alpha_water = pd.read_csv(os.path.join(folder_path, filename),
                                        header=0, delimiter='\t')
            depth = alpha_water.iloc[:, 0]
            alpha = alpha_water.iloc[:, 1]

            # Interpolation pour avoir la position où alpha.water = 0.5
            f = scipy.interpolate.interp1d(alpha, depth)
            interface = f(0.5).item()
            df.at[float(folder), probename] = interface
    print('done.')

    # normalisation des résultats pour avoir un signal centré en y=0
    if normalize:
        df -= df.iloc[0, 0]

    # Sauvegarde des résultats
    print('Sauvegarde dans {}'.format(outputFile))
    df.to_csv(outputFile, sep=',', index_label='time')
