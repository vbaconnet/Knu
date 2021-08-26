#!/usr/bin/env python3

"""
Lecture des fichiers sondes dans les fichiers postProcessing/line
"""

import os
import pandas as pd
import outilsLecture as olec
import outilsDivers as odiv
import sys


if __name__ == "__main__":

    #==========================================================================
    #------------------- Lecture des options ----------------------------------
    #==========================================================================


    cloudname  = olec.readValueOption(sys.argv, ["-cloudname","--cloudname"],
                                      default = None)

    #Read output file option
    outputFile = olec.readFileOption(sys.argv, ["-output","--output",
                                                "-outputFile","--outputFile"],
                                    default = "line_probes.csv",
                                    extension = "csv")
    

    #==========================================================================
    #------------------- Initialisation et intervalle de temps ----------------
    #==========================================================================

    # Dossier postProcessing
    cwd = 'postProcessing/points'

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
    #-------------------------- Traitement des clouds ------------------------
    #==========================================================================

    if cloudname is None:
        dirs = os.listdir(os.path.join(cwd, all_folders[0]))
        clouds = [i for i in dirs if i.endswith("p.xy")]
        if len(clouds) > 1:
            print("Clouds disponibles : ", clouds)
            print("Relancez le script avec le cloudname de votre choix : ")
            print("     lirePoints.py --cloudname <my_cloud>")
        elif len(clouds) == 1:
            cloudname = clouds[0]
            print(f'{cloudname} sélectionné')
        else:
            raise FileNotFoundError("Aucun cloud existant")

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
            data = pd.read_csv(cloudfilepath, header = None, delimiter = '\t')
            print("Extraction {} / {}".format(idx,len(all_folders)))
            pointIds = data.iloc[:,0]
            df.at[float(folder),:] = data.iloc[:,1]
    
    print("Sauvegarde dans {}".format(cloudname.split('_')[0]+".csv"))
    df.to_csv(cloudname.split('_')[0]+".csv", sep=",", index_label="time")

