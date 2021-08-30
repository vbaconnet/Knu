#!/usr/bin/env python3
"""
Informations
============

    * Auteur: Victor Baconnet
    * Date de dernière modification: 27 août 2021

Description
============

Rééchantillonne un signal avec une fréquence par défaut de 50 Hz, mais peut être
changée avec l'option ``--samplingfreq <freq>``

Entrées/sorties
================

*  Lecture des valeurs à traiter dans un fichier par défaut ``line_probes.csv``,
   mais peut être modifié avec la commande ``--file file.csv``. Le fichier
   doit être formaté comme suit::
       
       temps,val1,val2
       t1,v11,v12
       t2,v21,v22
       ...
       tn,vn1,vn2

   où les ``tn,vn1,vn2`` sont des valeurs numériques.

*  Données rééchantillonnées écrites dans le fichier dont le préfixe est 
   ``RESAMPLED_``, suivi du nom du fichier original.

Utilisation
============

--file file             Nom du fichier dans lequel lire le signal à traiter.
                        Doit être au format ``.csv``.
--samplingfreq freq     Fréquence de rééchantillonnage. Par défaut à 50 Hz  

Code source
============

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Post-traitement/resample.py>`_

"""

import numpy as np
from scipy import interpolate
import outilsLecture as olec
import sys
import os
import pandas as pd

if __name__ == "__main__":

    #Lecture du fichier source (.csv)
    file = olec.readFileOption(sys.argv, ["--file","-file"],
                            default = "line_probes.csv",
                            extension = "csv")

    #Donne une fréquence d'échantillonnage pour rééchantillonner le signal
    samplingFreq = olec.readValueOption(sys.argv, ["-samplingfreq", "--samplingfreq"],
                                        default = 50.0,
                                        valueType = float)


    #Récupérer les données de mesure des sondes
    if os.path.exists(file):
        print("Lecture dans {}".format(file))
        data = pd.read_csv(file)
        data.set_index(data.columns[0], inplace = True) #Pour mettre le temps comme index
    else:
        raise NameError("\n{} n'existe pas".format(file))

    #Nombre de sondes
    Nsondes = len(data.columns)

    print("\n{} sondes détectées".format(Nsondes))

    #On récupère le temps final
    time_read = data.index.values
    tmax = time_read[-1]

    # Calcul du pas de temps à la fréquence d'échantillonnage donnée
    timestep = 1.0/samplingFreq

    # Vecteur temps échantillonné tous les pas de temps. Exemple [0.02, 0.04, 0.06, ... , tmax]
    new_N = int(np.floor(tmax/timestep))
    time = np.linspace(timestep, new_N*timestep, new_N)
    #time = np.arange(timestep, (new_N+1)*timestep, timestep)

    #Récupère les valeurs des sondes
    valeursSondes_read = data.values     

    #Initialisation du tableau qui contiendra les valeurs rééchantillonnées
    valeursSondes = np.zeros( (new_N, Nsondes) )

    print("Temps maximal : {}".format(tmax))
    print("Fréquence d'échantillonnage : {}".format(samplingFreq))
    print("Nombre de points avant rééchantillonnage : {}".format(len(valeursSondes_read[:,0])))
    print("Nombre de points après rééchantillonnage : {}".format(new_N))


    # Interpolation pour échantillonner à la fréquence donnée
    for i in range(Nsondes):
        f = interpolate.interp1d(time_read, valeursSondes_read[:,i])
        valeursSondes[:,i] = f(time)

    reSampledData = pd.DataFrame(data = valeursSondes,
                                columns = data.columns,
                                index = time)

    reSampledData.index.name = data.index.name

    reSampledData.to_csv("RESAMPLED_"+file)
