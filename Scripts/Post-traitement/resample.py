#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:41:42 2021

@author: vbaconnet
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import outilsLecture as olec
import sys
import os
import pandas as pd

#Lecture du fichier source (.csv)
file = olec.readFileOption(sys.argv, ["--file","-file"],
                           default = "line_probes.csv",
                           extension = "csv")

#Donne une fréquence d'échantillonnage pour rééchantillonner le signal
samplingFreq = olec.readValueOption(sys.argv, ["-samplingFreq", "--samplingFreq"],
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