#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 14:12:22 2021

@author: Victor Baconnet

@contact:victor.baconnet@acri-in.fr

https://github.com/victor13165/

All rights reserved

Que fait ce programme? (spectre.py)
----------------------------------

Reconstruit et affiche les spectres de densité de puissance à partir de mesures de sondes 


Entrées/sorties
---------------

1. Les mesures des sondes doivent être données dans un fichier au format csv, par défaut
"line_probes.csv" mais peut être modifié avec l'option -sondeFile

2. Si vous souhaitez comparer les spectres calculés avec un spectre théorique de JONSWAP,
les paramètres Tp, Hs, Tmin, Tmax, gamma doivent être donnés dans un fichier par défaut 
"jonswapDict", mais peut être modifié avec l'option -jonswapFile


Ce programme peut s'éxecuter avec les options suivantes:
--------------------------------------------------------
    
    - --savefigs : Permet de sauvegarder les graphiques générés

    - --sondeFile chemin/vers/fichier.csv : chemin d'accès vers le fichier sondes au format csv 
    
    - --jonswapFile chemin/vers/fichier : chemin d'accès vers le fichier paramètres JONSWAP
    
    - --Npoints n : Nombre de points (longueur) de chaque segment de calcul par la méthode de 
    Welch (https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html#r34b375daf612-1)
    

Exemples d'utilisation (à lancer dans un terminal)
--------------------------------------------------

python3 spectre.py 

    --> Lit fichier sondes line_probes.csv et jonswapDict

python3 spectre.py --sondeFile sondes.csv 

    --> lit le fichier sondes sondes.csv et jonswapDict

python3 spectre.py --jonswapFile jonswapParams 

    --> lit le fichier sondes line_probes.csv et paramètres jonswap dans jonswapParams

Dépendances (les modules qu'il faut avoir installé au préalable)
----------------------------------------------------------------

    - numpy : s'installe avec 
    
                pip install numpy
                
    - scipy : s'installe avec
        
                pip install scipy
        
    - matplotlib : s'installe avec
        
                pip install matplotlib
            
    - pandas : s'installe avec
        
                pip install pandas
    
    - jonswap, genWaveProperties, outilsParaview, outilsLecture, outilsDivers : il faut avoir les 
    fichiers respectifs dans le répertoire à partir duquel vous exécutez votre programme, 
    ou mettre leur chemin d'accès dans la variable $PYTHONPATH. 
    
        export PYTHONPATH=/chemin/vers/dossier_jonswap:chemin/vers/dossier_outils:$PYTHONPATH
    
    S'installe en clonant le répertoire à partir de GitHub : 
        
                git clone https://github.com/victor13165/scripts-python-ACRI

"""

#------- ces modules sont indispensables -----
import sys
import numpy as np
import jonswap as jswp #le fichier jonswap.py doit être dans le même dossier
import genWaveProperties as gwp
import os
import outilsLecture as olec
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import outilsDivers as odiv
#---------------------------------------------


def getSondeData(sondeFile, tmin, tmax):
    """
    Lecture des mesures de sondes dans le fichier sondeFile (le plus souvent sondes.csv)
    
    Paramètres d'entrée:
    --------------------
        - sondeFile (string) : Nom du fichier .csv où il y a le résultat des sondes
        - tmin, tmax (float) : Temps minimal et maximal d'affichage
    
    Sortie:
    -------
        - DataFrame avec les valeurs et les noms des sondes 
    """
            
    sondeData = pd.read_csv(sondeFile) #ouvrir le fichier
    
    time = sondeData.columns[0] #Récupérer le nom de la colonne du temps. Par sécurité, on ne prend pas ['time[s]']
    
    #Récupérer les indices des temps min et max
    minIdx = odiv.find(sondeData[time], tmin, 0)
    maxIdx = odiv.find(sondeData[time], tmax, -1) 
    
    if maxIdx == -1 : #Valeur max par défaut
        return sondeData[minIdx:]    #on prend jusqu'à la fin, car sondeData[i:-1] ne prend pas le dernier élément
    else:
        return sondeData[minIdx:maxIdx+1] #Dans ce cas on peut aller jusqu'à l'élément que l'on souhaite
                                          #Rappel: tab[a,b] renvoie tab de l'indice a jusqu'à l'indice b-1



if __name__ == "__main__":

    #+++++++++++++++++++++++++ Lecture des options ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    print("\nLecture des options")
    print("--------------------------")
    
    #Sauvegarde des figures?
    savefigs = olec.readOption(sys.argv, ['-savefigs','--savefigs'])
    
    #Fichier jonswapDict contenant les paramètres du spectre de jonswap
    jonswapFile = olec.readFileOption(sys.argv, ['-jonswapFile','--jonswapFile'],
                                      default = "jonswapDict")
    
    #Fichier .csv qui contient le résultat des mesures des sondes en fonction du temps
    sondeFile   = olec.readFileOption(sys.argv, ['-sondeFile','--sondeFile', 
                                                 '--sondesFile', '-sondesFile'],
                                      default = "line_probes.csv")
    
    #Nombre de points (longueur) de chaque segment de calcul par la méthode de Welch
    Npoints = olec.readValueOption(sys.argv, ["-Npoints", "--Npoints"],
                                   default = 1024,
                                   valueType = int)
    
    print("---------------------------")
    print("Fin de lecture des options")
    
    #=============================================================================================================
    
    print("\nLecture du fichier {}".format(sondeFile))
    
    #Récupérer les données de mesure des sondes
    if os.path.exists(sondeFile):
        
        sondeData = pd.read_csv(sondeFile)
        sondeData.set_index(sondeData.columns[0], inplace = True) #Pour mettre le temps comme index
        
    else:
        raise NameError("\n{} n'existe pas".format(sondeFile))

    #Nombre de sondes
    Nsondes = len(sondeData.columns)

    print("\n{} sondes détectées".format(Nsondes))

    #On récupère le temps final
    time = sondeData.index.values
    tmax = time[-1]

    # Calcul du pas de temps supposé constant
    timestep = time[1] - time[0]
    print("Pas de temps :  {}".format(timestep))

    #Fréquence d'échantillonnage
    samplingFreq = 1.0/timestep
    print("Fréquence d'échantillonnage : {}".format(samplingFreq))

    #Récupère les valeurs des sondes
    valeursSondes = sondeData.values

    #Calcul du premier spectre pour déterminer la taille de chaque spectre
    f, p0 = signal.welch(valeursSondes[:,0], samplingFreq, nperseg = Npoints)   
    
    #Va contenir les spectres de densité de puissance de chaque sonde
    spectresSondes = np.zeros((len(p0), Nsondes)) 
    
    print("\nCalcul des spectres de chaque sonde")
    
    #Calcul du spectre |X|² pour chaque sonde
    for i in range(Nsondes):
        print("Sonde {}/{}".format(i,Nsondes))
        f, spectresSondes[:,i] = signal.welch(valeursSondes[:,i], samplingFreq, nperseg = Npoints)
    
    #Conversion Hz en rad/s
    w = 2.0*np.pi*f
    spectresSondes /= 2.0*np.pi #Facteur 1/2pi pour passer en rad/s
    
    #------------------------------- Tracé ---------------------------------------------
    plt.figure(figsize=(8,7))
    
    for i in range(Nsondes):
        plt.plot(w, spectresSondes[:,i], label = "{}".format(sondeData.columns[i]))
    
    
    plt.xlabel(r"$\omega$ (rad $s^{-1}$)", fontsize = 17)
    plt.ylabel(r"$S(\omega)$ ($m^2$ s)"     , fontsize = 17)
    plt.title("Spectre reconstruit par chaque sonde", fontsize = 17)
    plt.tick_params(axis = 'both', which = "major", labelsize = 15)
    plt.grid()
    
    
    #Si on trouve le fichier contenant les paramètres Tp, Hs, etc, on peut tracer le spectre idéal
    if os.path.exists(jonswapFile):
        
        print("\n{} trouvé".format(jonswapFile))
        
        #Lecture des paramètres donnés dans jonswapDict
        param_dict = gwp.readParams(jonswapFile)
        
        Tmin,Tmax,Tp = param_dict["tmin"], param_dict["tmax"], param_dict["tp"]
        Hs,gamma = param_dict["hs"],param_dict["gamma"]   
          
        wmin = 2.0*np.pi/Tmax   #Fréquence min
        wmax = 2.0*np.pi/Tmin   #Fréquence max
        plt.xlim((wmin,wmax))
            
        #Enlever le premier élement de w si il vaut 0
        if abs(w[0]) < 1e-8:
            w = w[1:]
            
        #Calcul du spectre de JONSWAP
        spectre = jswp.jonswap(Hs, Tp, gamma, w)
        
        plt.plot(w, spectre, label = "Spectre idéal")
        plt.legend(fontsize = 16)
        plt.tight_layout()
        
        
        #Calcul de l'erreur quadratique moyenne par rapport au spectre inlet
        err_moy = 0.0
        spectreRef = None
        inletIdx = None

        #Chercher si la sonde "inlet" existe
        for idx, i in enumerate(sondeData.columns):
            if i.split("-")[0].lower() == "inlet" \
                or i.split("_")[0].lower() == "inlet":
                spectreRef = spectresSondes[1:,idx]
                inletIdx = idx
                print("\n---- Erreur quadratique moyenne (RMSE) avec le spectre INLET -----")
                break
        
        if spectreRef is None:
            spectreRef = spectre
            print("\n---- Erreur quadratique moyenne (RMSE) avec le spectre idéal -----")
        
        NsondesMoyenne = 0
        for i in range(Nsondes):
            if i != inletIdx:
                NsondesMoyenne += 1
                err = odiv.RMSE(spectreRef,spectresSondes[1:,i])
                err_moy += err 
                print("{} : {}".format(sondeData.columns[i], err))
        print("\nMoyenne : {}".format(err_moy/NsondesMoyenne))
        print(  "+------------------------------------------------------------------")
        
        if savefigs:
            if os.path.exists("postProcessing"):
                dirname = "postProcessing"
            else:
                dirname = "."
             
            saveFilePath = os.path.join(dirname,
                                        "spectre_sondes_N{}_{}.png".format(
                                            Npoints, datetime.now().strftime("%d-%m_%H-%M-%S")))
            
            print("Sauvegarde du graphe dans {}".format(saveFilePath))
            plt.savefig(saveFilePath)  
            
        plt.show()
    
    else:
        print("{} n'existe pas".format(jonswapFile))
        plt.legend(fontsize = 16)
        plt.tight_layout()
        if savefigs:
            if os.path.exists("postProcessing"):
                dirname = "postProcessing"
            else:
                dirname = "."
             
            saveFilePath = os.path.join(dirname,
                                        "spectre_sondes_N{}_{}.png".format(
                                            Npoints, datetime.now().strftime("%d-%m_%H-%M-%S")))
            
            print("Sauvegarde du graphe dans {}".format(saveFilePath))
            plt.savefig(saveFilePath)  
      
    
        plt.show()
      
    #-----------------------------------------------------------------------------------
