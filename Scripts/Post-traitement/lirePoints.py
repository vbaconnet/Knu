#!/usr/bin/env python3

"""
Informations
============

    * Fichier : ``Knu/Scripts/Post-traitement/lirePoints.py``
    * Auteur: Victor Baconnet
    * Date de dernière modification: 27 août 2021

Description
============

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

--outputfile file       Fichier de sortie des mesures de sondes
--name name             Nom du dossier où se trouvent les mesures. Ce nom correspond
                        au chemin ``postProcessing/<name>``.
--champ champ           Champ de données à lire. Exemple de champs: 
                        ``alpha.water``, ``p``, ``U``...
--cloudname cloud       Nom du cloud de points. Ce nom du cloud correspond au
                        nom de fichier de type ``<cloud>_<champ>.xy``

Dépendances
============

* ``pandas``
* ``outilsLecture``, ``outilsDivers``
* ``sys``, ``os`` 

Code source
============

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Post-traitement/lirePoints.py>`_
"""

from numpy import genfromtxt
import os
import pandas as pd
import outilsLecture as olec
import outilsDivers as odiv
import sys


if __name__ == "__main__":

    #==========================================================================
    #------------------- Lecture des options ----------------------------------
    #==========================================================================

    # Nom du set où tous les points sont stockés
    name = olec.readDirOption(sys.argv, ["--pointname", "-pointname"],
                              "points")

    # Nom du cloud
    cloudname  = olec.readValueOption(sys.argv, ["-name","--name"],
                                      default = None,
                                      valueType=str)
    
    # Choix du champ à lire
    field = olec.readValueOption(sys.argv,
                                 ["--champ", "-champ"],
                                 default="p",
                                 valueType=str)

    #==========================================================================
    #------------------- Initialisation et intervalle de temps ----------------
    #==========================================================================

    # Dossier postProcessing
    cwd = 'postProcessing/'+name

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
    #-------------------------- Traitement des clouds ------------------------
    #==========================================================================

    if cloudname is None:
        dirs = os.listdir(os.path.join(cwd, all_folders[0]))
        clouds = [i for i in dirs if i.endswith(field+".xy")]
        
        if len(clouds) > 1:
            print("Clouds disponibles : ", clouds)
            print("Relancez le script avec le cloudname de votre choix : ")
            print("     lirePoints.py --cloudname <my_cloud>")
            exit()
        elif len(clouds) == 1:
            cloudname = clouds[0]
            print(f'{cloudname} sélectionné')
        else:
            raise FileNotFoundError("Aucun cloud existant. Vérifiez que le champ\
 {} est valide".format(field))

    # Aller chercher le nombre de points dans le tout premier fichier
    cloudfile  = os.listdir(os.path.join(cwd, all_folders[0]))[0]
    cloudfilepath = os.path.join(cwd,all_folders[0],cloudfile)
    temp = pd.read_csv(cloudfilepath, header = None, delimiter = '\t')
    pointIds = temp.iloc[:,0]
    
    # Creation du dataframe
    df = pd.DataFrame(index = time_vec, columns = pointIds)

    for idx, folder in enumerate(all_folders, 1):
        for cloudfile in os.listdir(os.path.join(cwd, folder)):
            
            cloudfilepath = os.path.join(cwd,folder,cloudfile)
            data = genfromtxt(cloudfilepath)
            print("Extraction {} / {}".format(idx,len(all_folders)))
            pointIds = [i[0] for i in data]
            df.at[float(folder),:] = [i[1] for i in data]
    
    print("Sauvegarde dans {}".format(cloudname.split('_')[0]+".csv"))
    df.to_csv(cloudname.split('_')[0]+".csv", sep=",", index_label="time")

